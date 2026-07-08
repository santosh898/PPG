"use client";

import { useEffect, useRef } from "react";
import "leaflet/dist/leaflet.css";

export interface HeatPoint {
  lat: number;
  lng: number;
  weight: number;
  label: string;
  category: string;
  priority_score: number;
}

type LatLng = [number, number];

interface LeafletMap {
  setView: (center: LatLng, zoom: number) => LeafletMap;
  eachLayer: (fn: (layer: LeafletLayer) => void) => void;
  removeLayer: (layer: LeafletLayer) => void;
  fitBounds: (bounds: unknown) => void;
}

interface LeafletLayer {
  addTo: (map: LeafletMap) => LeafletLayer;
  bindPopup?: (html: string) => LeafletLayer;
  _heat?: unknown;
  _icon?: unknown;
}

interface LeafletApi {
  map: (el: HTMLElement) => LeafletMap;
  tileLayer: (url: string, opts: Record<string, unknown>) => LeafletLayer;
  heatLayer: (data: number[][], opts: Record<string, unknown>) => LeafletLayer;
  circleMarker: (center: LatLng, opts: Record<string, unknown>) => LeafletLayer;
  latLngBounds: (points: LatLng[]) => { pad: (n: number) => unknown };
  CircleMarker: unknown;
}

/**
 * Leaflet + OpenStreetMap heatmap (no API key). Loaded client-side only via
 * next/dynamic in the parent, so Leaflet never runs on the server.
 */
export default function HeatMap({ points }: { points: HeatPoint[] }) {
  const containerRef = useRef<HTMLDivElement>(null);
  const mapRef = useRef<LeafletMap | null>(null);

  useEffect(() => {
    let cancelled = false;

    async function init() {
      const mod = await import("leaflet");
      await import("leaflet.heat");
      if (cancelled || !containerRef.current) return;

      const L = (mod.default ?? mod) as unknown as LeafletApi;

      if (!mapRef.current) {
        const center: LatLng =
          points.length > 0 ? [points[0].lat, points[0].lng] : [17.72, 83.3];
        const map = L.map(containerRef.current).setView(center, 12);
        L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
          attribution: "&copy; OpenStreetMap contributors",
          maxZoom: 19,
        }).addTo(map);
        mapRef.current = map;
      }

      const map = mapRef.current;

      map.eachLayer((layer) => {
        if (layer._heat || layer._icon) {
          map.removeLayer(layer);
        }
      });

      const maxWeight = Math.max(1, ...points.map((p) => p.weight));
      const heatData = points.map(
        (p) => [p.lat, p.lng, p.weight / maxWeight] as number[]
      );
      L.heatLayer(heatData, { radius: 35, blur: 20, maxZoom: 14 }).addTo(map);

      for (const p of points) {
        const marker = L.circleMarker([p.lat, p.lng], {
          radius: 6,
          color: "#1d61f1",
          fillColor: "#3380fc",
          fillOpacity: 0.8,
        });
        marker.bindPopup?.(
          `<strong>${p.label}</strong><br/>${p.category} · ${p.weight} submissions · score ${p.priority_score}`
        );
        marker.addTo(map);
      }

      if (points.length > 1) {
        const bounds = L.latLngBounds(points.map((p) => [p.lat, p.lng] as LatLng));
        map.fitBounds(bounds.pad(0.2));
      }
    }

    init();
    return () => {
      cancelled = true;
    };
  }, [points]);

  return (
    <div
      ref={containerRef}
      className="h-[420px] w-full rounded-xl border border-slate-200"
      style={{ zIndex: 0 }}
    />
  );
}
