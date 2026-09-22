"""
================================================================================
GENERADOR DE MODELO 3D ANATÓMICO PÉLVICO REAL (glTF 2.0 / .GLB)
BioPelvis Pro - Suite Biomecánica Sacroilíaca
Origen de Mallas: Segmentación Tomográfica Real (Johns Hopkins PelvisAtlas / CC)
Nodos independientes:
  - 'Sacrum' (Sacro central fijo)
  - 'Hip_L'  (Ilíaco / Coxal izquierdo articulado)
  - 'Hip_R'  (Ilíaco / Coxal derecho articulado)
================================================================================
"""

import json
import os
import struct
import urllib.request
import numpy as np


def download_vtk_surface(url: str) -> str:
    """Descarga superficie de malla anatómica en formato VTK PolyData."""
    req = urllib.request.Request(url, headers={'User-Agent': 'BioPelvis-Atlas/1.0'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode('ascii', errors='ignore')


def parse_vtk_polydata(content: str):
    """Parsea vértices y triángulos a partir de texto VTK PolyData."""
    lines = content.splitlines()
    points = []
    triangles = []
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith('POINTS'):
            parts = line.split()
            n_points = int(parts[1])
            i += 1
            pts_vals = []
            while len(pts_vals) < n_points * 3 and i < len(lines):
                cur_line = lines[i].strip()
                if cur_line.startswith(('POLYGONS', 'CELLS', 'LINES')):
                    break
                pts_vals.extend([float(x) for x in cur_line.split()])
                i += 1
            points = np.array(pts_vals[:n_points * 3], dtype=np.float32).reshape((n_points, 3))
            continue
            
        if line.startswith('POLYGONS'):
            parts = line.split()
            n_polys = int(parts[1])
            i += 1
            while len(triangles) < n_polys and i < len(lines):
                cur_line = lines[i].strip()
                if not cur_line or cur_line.startswith(('POINT_DATA', 'CELL_DATA')):
                    break
                toks = [int(x) for x in cur_line.split()]
                if len(toks) == 4 and toks[0] == 3:
                    triangles.append(toks[1:4])
                i += 1
            triangles = np.array(triangles, dtype=np.uint32)
            continue
        i += 1
        
    return points, triangles


def build_anatomical_pelvis_glb(
    output_path_primary: str = "models/pelvis_anatomica.glb",
    output_path_secondary: str = "assets/pelvis.glb"
):
    """
    Descarga o procesa las mallas óseas de tomografía computarizada (CT) y compila
    un archivo glTF 2.0 binario (.glb) estructurado con nodos independientes.
    """
    os.makedirs(os.path.dirname(output_path_primary), exist_ok=True)
    os.makedirs(os.path.dirname(output_path_secondary), exist_ok=True)

    sacrum_url = 'https://raw.githubusercontent.com/I-STAR/PelvisAtlas/main/surface/sacrum/Sacrum11_cpd.vtk'
    lh_url = 'https://raw.githubusercontent.com/I-STAR/PelvisAtlas/main/surface/left/LeftHip11_cpd.vtk'
    rh_url = 'https://raw.githubusercontent.com/I-STAR/PelvisAtlas/main/surface/right/RightHip11_cpd.vtk'

    print("Descargando superficies anatómicas del atlas tomográfico...")
    s_pts, s_tris = parse_vtk_polydata(download_vtk_surface(sacrum_url))
    l_pts, l_tris = parse_vtk_polydata(download_vtk_surface(lh_url))
    r_pts, r_tris = parse_vtk_polydata(download_vtk_surface(rh_url))

    # Centrado y normalización de escala a unidades Three.js (~1.6 unidades de altura)
    all_pts = np.vstack([s_pts, l_pts, r_pts])
    center = all_pts.mean(axis=0)
    height = all_pts[:, 2].max() - all_pts[:, 2].min()
    scale = 1.6 / height

    def to_threejs(pts):
        # Conversión del sistema radiológico DICOM/CT a Three.js:
        # X: Lateral (+X Izquierda anatómica del paciente, -X Derecha anatómica)
        # Y: Craneal/Superior (+Y)
        # Z: Anterior (+Z anterior, -Z posterior)
        x = (pts[:, 0] - center[0]) * scale
        y = (pts[:, 2] - center[2]) * scale
        z = -(pts[:, 1] - center[1]) * scale
        return np.column_stack([x, y, z]).astype(np.float32)

    s_pos = to_threejs(s_pts)
    l_pos = to_threejs(l_pts)
    r_pos = to_threejs(r_pts)

    # Invertir bobinado de triángulos para caras exteriores frontales normales
    s_ind = s_tris[:, [0, 2, 1]].flatten().astype(np.uint16)
    l_ind = l_tris[:, [0, 2, 1]].flatten().astype(np.uint16)
    r_ind = r_tris[:, [0, 2, 1]].flatten().astype(np.uint16)

    parts = [
        ("Sacrum", s_pos, s_ind),
        ("Hip_L", l_pos, l_ind),
        ("Hip_R", r_pos, r_ind),
    ]

    binary_chunks = []
    buffer_views = []
    accessors = []
    meshes = []
    nodes = []

    current_byte_offset = 0

    for i, (name, pos, ind) in enumerate(parts):
        # Buffer de posiciones
        pos_bytes = pos.tobytes()
        pos_min = pos.min(axis=0).tolist()
        pos_max = pos.max(axis=0).tolist()
        pad = (4 - (len(pos_bytes) % 4)) % 4
        pos_bytes += b'\x00' * pad

        bv_pos_idx = len(buffer_views)
        buffer_views.append({
            "buffer": 0,
            "byteOffset": current_byte_offset,
            "byteLength": len(pos.tobytes()),
            "target": 34962 # ARRAY_BUFFER
        })
        current_byte_offset += len(pos_bytes)
        binary_chunks.append(pos_bytes)

        acc_pos_idx = len(accessors)
        accessors.append({
            "bufferView": bv_pos_idx,
            "byteOffset": 0,
            "componentType": 5126, # FLOAT
            "count": len(pos),
            "type": "VEC3",
            "min": pos_min,
            "max": pos_max
        })

        # Buffer de índices triangulares
        ind_bytes = ind.tobytes()
        pad = (4 - (len(ind_bytes) % 4)) % 4
        ind_bytes += b'\x00' * pad

        bv_ind_idx = len(buffer_views)
        buffer_views.append({
            "buffer": 0,
            "byteOffset": current_byte_offset,
            "byteLength": len(ind.tobytes()),
            "target": 34963 # ELEMENT_ARRAY_BUFFER
        })
        current_byte_offset += len(ind_bytes)
        binary_chunks.append(ind_bytes)

        acc_ind_idx = len(accessors)
        accessors.append({
            "bufferView": bv_ind_idx,
            "byteOffset": 0,
            "componentType": 5123, # UNSIGNED_SHORT
            "count": len(ind),
            "type": "SCALAR",
            "min": [int(ind.min())],
            "max": [int(ind.max())]
        })

        mesh_idx = len(meshes)
        meshes.append({
            "name": name,
            "primitives": [{
                "attributes": {"POSITION": acc_pos_idx},
                "indices": acc_ind_idx,
                "material": 0
            }]
        })

        node_idx = len(nodes)
        nodes.append({
            "name": name,
            "mesh": mesh_idx
        })

    total_bin_data = b''.join(binary_chunks)

    # Material de hueso médico marfil (color: 0xe8e4dc, roughness: 0.6)
    gltf_dict = {
        "asset": {"version": "2.0", "generator": "BioPelvis Pro Anatomical CT Pipeline"},
        "scene": 0,
        "scenes": [{"name": "PelvisScene", "nodes": list(range(len(nodes)))}],
        "nodes": nodes,
        "meshes": meshes,
        "accessors": accessors,
        "bufferViews": buffer_views,
        "buffers": [{"byteLength": len(total_bin_data)}],
        "materials": [{
            "name": "BoneMarfilMaterial",
            "pbrMetallicRoughness": {
                "baseColorFactor": [0.91, 0.894, 0.863, 1.0],
                "roughnessFactor": 0.6,
                "metallicFactor": 0.05
            },
            "doubleSided": True
        }]
    }

    json_bytes = json.dumps(gltf_dict, separators=(',', ':')).encode('utf-8')
    pad_json = (4 - (len(json_bytes) % 4)) % 4
    json_bytes += b' ' * pad_json

    glb_header = struct.pack("<4sII", b"glTF", 2, 12 + 8 + len(json_bytes) + 8 + len(total_bin_data))
    json_header = struct.pack("<II", len(json_bytes), 0x4E4F534A)
    bin_header = struct.pack("<II", len(total_bin_data), 0x004E4942)

    glb_bytes = glb_header + json_header + json_bytes + bin_header + total_bin_data

    for out_p in [output_path_primary, output_path_secondary]:
        with open(out_p, "wb") as f:
            f.write(glb_bytes)
        print(f"Modelo anatómico generado: {out_p} ({len(glb_bytes):,} bytes)")

    return glb_bytes


if __name__ == "__main__":
    build_anatomical_pelvis_glb()
