#!/usr/bin/env python3
"""Generate a shortest-path route map from Mahamuni Buddha Temple to Zegyo Market.

The script uses OpenStreetMap data via OSMnx:
1. Geocode both landmarks.
2. Download a walking network around them.
3. Compute the shortest path by street length.
4. Render a static JPEG map with the route highlighted.
"""

from __future__ import annotations

import math
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import osmnx as ox


START_QUERY = "Mahamuni Buddha Temple, Mandalay, Myanmar"
END_QUERY = "Zegyo Market, Mandalay, Myanmar"
OUTPUT_PATH = Path("mahamuni_to_zegyo_shortest_path.jpg")


def meters_to_pad_meters(lat_span_deg: float, lon_span_deg: float, lat_center: float) -> float:
    """Return a conservative map padding in projected meters for the route extent."""
    lat_m = lat_span_deg * 111_320.0
    lon_m = lon_span_deg * 111_320.0 * math.cos(math.radians(lat_center))
    return max(lat_m, lon_m, 1_500.0)


def main() -> None:
    ox.settings.use_cache = True
    ox.settings.log_console = False

    start_lat, start_lon = ox.geocode(START_QUERY)
    end_lat, end_lon = ox.geocode(END_QUERY)

    mid_lat = (start_lat + end_lat) / 2
    mid_lon = (start_lon + end_lon) / 2

    # Large enough to contain alternative walking routes through Mandalay's center.
    graph = ox.graph_from_point((mid_lat, mid_lon), dist=6_000, network_type="walk", simplify=True)

    start_node = ox.distance.nearest_nodes(graph, X=start_lon, Y=start_lat)
    end_node = ox.distance.nearest_nodes(graph, X=end_lon, Y=end_lat)

    route = nx.shortest_path(graph, start_node, end_node, weight="length")
    route_length_m = nx.shortest_path_length(graph, start_node, end_node, weight="length")

    graph_proj = ox.project_graph(graph)
    nodes_proj = ox.graph_to_gdfs(graph_proj, edges=False)

    # Focus the map on the route itself instead of the whole graph footprint.
    route_nodes = nodes_proj.loc[route]
    lon_span = abs(end_lon - start_lon)
    lat_span = abs(end_lat - start_lat)
    pad_m = meters_to_pad_meters(lat_span, lon_span, mid_lat)

    fig, ax = ox.plot_graph_route(
        graph_proj,
        route,
        route_linewidth=5,
        route_color="#b00020",
        route_alpha=0.95,
        node_size=0,
        edge_color="#c7d0d9",
        edge_linewidth=0.6,
        bgcolor="#f7f4ee",
        show=False,
        close=False,
        figsize=(12, 10),
    )

    # Highlight origin and destination.
    origin = nodes_proj.loc[start_node]
    destination = nodes_proj.loc[end_node]
    ax.scatter(origin.x, origin.y, s=90, c="#1b5e20", edgecolors="white", linewidths=1.2, zorder=5)
    ax.scatter(destination.x, destination.y, s=90, c="#0d47a1", edgecolors="white", linewidths=1.2, zorder=5)
    ax.annotate(
        "Mahamuni Buddha Temple",
        xy=(origin.x, origin.y),
        xytext=(8, 10),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color="#1b5e20",
        zorder=6,
    )
    ax.annotate(
        "Zegyo Market",
        xy=(destination.x, destination.y),
        xytext=(8, -16),
        textcoords="offset points",
        fontsize=10,
        fontweight="bold",
        color="#0d47a1",
        zorder=6,
    )

    minx, miny, maxx, maxy = route_nodes.total_bounds
    ax.set_xlim(minx - pad_m, maxx + pad_m)
    ax.set_ylim(miny - pad_m, maxy + pad_m)

    ax.set_title(
        f"Shortest walking path: Mahamuni Buddha Temple to Zegyo Market\n"
        f"Route length: {route_length_m/1000:.2f} km",
        fontsize=16,
        fontweight="bold",
        pad=16,
    )
    ax.text(
        0.02,
        0.02,
        "Source: OpenStreetMap walking network",
        transform=ax.transAxes,
        fontsize=9,
        color="#555555",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#dddddd", alpha=0.9),
    )

    fig.tight_layout()
    fig.savefig(OUTPUT_PATH, dpi=300, format="jpg", pil_kwargs={"quality": 95, "optimize": True})
    plt.close(fig)

    print(f"start=({start_lat:.7f}, {start_lon:.7f})")
    print(f"end=({end_lat:.7f}, {end_lon:.7f})")
    print(f"route_length_m={route_length_m:.1f}")
    print(f"route_nodes={len(route)}")
    print(f"saved={OUTPUT_PATH.resolve()}")


if __name__ == "__main__":
    main()
