"use client";

import { useEffect, useRef } from "react";
import { Lock } from "lucide-react";
import "leaflet/dist/leaflet.css";
import { CONSTITUENCY_MAP_BOUNDS, CONSTITUENCY_MAP_CENTER } from "@/lib/constants";

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
  eachLayer: (fn: (layer: LeafletLayer) => void) => void;
  removeLayer: (layer: LeafletLayer) => void;
}

interface LeafletLayer {
  addTo: (map: LeafletMap) => LeafletLayer;
  bindPopup?: (html: string) => LeafletLayer;
  _heat?: unknown;
  _icon?: unknown;
}

interface LeafletApi {
  map: (el: HTMLElement, opts: Record<string, unknown>) => LeafletMap;
  tileLayer: (url: string, opts: Record<string, unknown>) => LeafletLayer;
  heatLayer: (data: number[][], opts: Record<string, unknown>) => LeafletLayer;
  circleMarker: (center: LatLng, opts: Record<string, unknown>) => LeafletLayer;
  latLngBounds: (points: LatLng[]) => unknown;
}

/**
 * Leaflet + OpenStreetMap heatmap (no API key). Loaded client-side only via
 * next/dynamic in the parent, so Leaflet never runs on the server.
 *
 * This MVP is scoped to a single constituency (Visakhapatnam), so the map is
 * intentionally locked to that area via maxBounds/minZoom rather than
 * re-fitting to wherever the data happens to be — there is nothing else to
 * pan to.
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
        const bounds = L.latLngBounds(CONSTITUENCY_MAP_BOUNDS);
        const map = L.map(containerRef.current, {
          center: CONSTITUENCY_MAP_CENTER,
          zoom: 12,
          minZoom: 11,
          maxZoom: 17,
          maxBounds: bounds,
          maxBoundsViscosity: 1.0,
        });
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
    }

    init();
    return () => {
      cancelled = true;
    };
  }, [points]);

  return (
    <div className="relative">
      <div
        ref={containerRef}
        className="h-[420px] w-full rounded-xl border border-slate-200"
        style={{ zIndex: 0 }}
      />
      <div className="pointer-events-none absolute left-3 top-3 z-[400] flex items-center gap-1.5 rounded-full bg-white/95 px-3 py-1.5 text-xs font-medium text-slate-600 shadow-soft">
        <Lock className="h-3.5 w-3.5 text-slate-400" />
        Visakhapatnam constituency (fixed view)
      </div>
      <div className="pointer-events-none absolute bottom-3 right-3 z-[400] flex items-center gap-2 rounded-full bg-white/95 px-3 py-1.5 text-xs text-slate-500 shadow-soft">
        <span className="h-2.5 w-2.5 rounded-full bg-brand-500" />
        Report density
        <span className="mx-1 h-3 w-px bg-slate-200" />
        <span className="h-2.5 w-2.5 rounded-full border-2 border-brand-600 bg-white" />
        Cluster
      </div>
    </div>
  );
}
