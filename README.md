# Mahamuni Buddha Temple to Zegyo Market Route Map

This project computes the shortest walking path between **Mahamuni Buddha Temple** and **Zegyo Market** in Mandalay, Myanmar, using OpenStreetMap street data. It renders the result as a static **JPEG map** with the route highlighted.

The repository is intentionally small:

- `generate_route_map.py` downloads the OSM network, computes the route, and exports the map.
- `mahamuni_to_zegyo_shortest_path.jpg` is the generated deliverable.

## What The Map Shows

- The shortest path by street length on the **walkable** OpenStreetMap network.
- The origin and destination locations.
- A route title with the measured distance.
- A light street backdrop and a highlighted route line for quick visual inspection.

## Output

Running the generator produces:

- `mahamuni_to_zegyo_shortest_path.jpg`

In the current generated version, the route length is approximately:

- `3.70 km`

## Method

The script performs these steps:

1. Geocodes both landmarks with OpenStreetMap's Nominatim service through OSMnx.
2. Downloads a walking street network around the route area from OpenStreetMap via Overpass.
3. Finds the nearest graph nodes to the two landmarks.
4. Computes the shortest path using edge length as the weight.
5. Projects the graph for plotting and renders a static JPEG.

## Requirements

- Python `3.12` or newer
- Network access on first run, so OSM data can be downloaded

Python dependencies are listed in [`requirements.txt`](requirements.txt):

- `osmnx`
- `networkx`
- `matplotlib`
- `pillow`
- `scikit-learn`

## Quick Start

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python generate_route_map.py
```

After the script finishes, open:

- [`mahamuni_to_zegyo_shortest_path.jpg`](mahamuni_to_zegyo_shortest_path.jpg)

## Reproducing The Result

The script is deterministic with respect to the live OpenStreetMap data available at run time, but the exact route may change if the upstream map data changes.

If you want to regenerate the map later:

```bash
source .venv/bin/activate
python generate_route_map.py
```

The script will:

- reuse cached OSM responses when available
- overwrite the existing JPEG with a fresh render

## Project Layout

```text
.
├── generate_route_map.py
├── mahamuni_to_zegyo_shortest_path.jpg
├── requirements.txt
├── README.md
└── cache/
```

## Implementation Notes

- The route is computed on the **walking** network, not the driving network.
- The plotted map is focused on the route corridor, not the entire city graph.
- The output image is rendered at `300 DPI` in JPEG format.

## Data Attribution

OpenStreetMap data is used for geocoding and street routing.

- OpenStreetMap: <https://www.openstreetmap.org/>

## Files You May Want To Commit

For a clean GitHub repo, typically commit:

- `generate_route_map.py`
- `mahamuni_to_zegyo_shortest_path.jpg`
- `requirements.txt`
- `README.md`

You usually should not commit:

- `.venv/`
- `cache/`

