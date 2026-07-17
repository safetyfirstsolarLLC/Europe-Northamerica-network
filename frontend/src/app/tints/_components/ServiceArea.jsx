import { MapPin } from "lucide-react";

const AREAS = [
  { name: "Palm Springs", desc: "Historic estates, mid-century modern icons" },
  { name: "Palm Desert", desc: "Ironwood, Bighorn, Vintage Club" },
  { name: "Rancho Mirage", desc: "Thunderbird, Mission Hills" },
  { name: "La Quinta", desc: "Andalusia, Madison Club, Tradition" },
  { name: "Indian Wells", desc: "Toscana, The Reserve" },
  { name: "Coachella", desc: "Custom builds & desert retreats" },
  { name: "Twentynine Palms", desc: "Off-grid & desert-modern homes" },
  { name: "Joshua Tree", desc: "Rammed-earth & designer homes" },
];

export default function ServiceArea() {
  return (
    <section id="service-area" data-testid="service-area-section" className="py-24 md:py-32 bg-surface/40 border-y border-white/5">
      <div className="max-w-7xl mx-auto px-6">
        <div className="max-w-2xl mb-14">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Where We Serve</div>
          <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight">
            From the Springs to the <span className="italic text-gold">high desert.</span>
          </h2>
          <p className="mt-4 text-white/60 font-light text-lg">
            Full mobile service across the Coachella Valley and Morongo Basin. Same-week appointments available.
          </p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-4 gap-0 border border-white/10">
          {AREAS.map((a, i) => (
            <div
              key={a.name}
              data-testid={`service-area-${i}`}
              className="p-6 border-r border-b border-white/10 last:border-r-0 hover:bg-gold/5 transition-colors"
            >
              <MapPin className="h-4 w-4 text-gold mb-3" strokeWidth={1.5} />
              <div className="font-serif text-xl text-white">{a.name}</div>
              <div className="text-white/50 text-xs mt-1 font-light">{a.desc}</div>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
