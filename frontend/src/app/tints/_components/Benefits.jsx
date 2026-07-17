import { TrendingDown, Home, Award, MapPin } from "lucide-react";

const BENEFITS = [
  { icon: TrendingDown, stat: "30%", label: "lower cooling bills", desc: "Reduce HVAC load through hottest desert months." },
  { icon: Home, stat: "82°F", label: "cooler window surface", desc: "Measurable relief within minutes of installation." },
  { icon: Award, stat: "15yr", label: "manufacturer warranty", desc: "Lifetime residential warranty on premium films." },
  { icon: MapPin, stat: "100%", label: "mobile service", desc: "We install on-site so your home is never disrupted." },
];

const IMG = "https://images.unsplash.com/photo-1709418354364-8f3e9ad5c32c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBkZXNlcnQlMjBsdXh1cnklMjBob21lJTIwZXh0ZXJpb3IlMjBwYWxtJTIwc3ByaW5nc3xlbnwwfHx8fDE3ODMxMDg4ODd8MA&ixlib=rb-4.1.0&q=85";

export default function Benefits() {
  return (
    <section data-testid="benefits-section" className="py-24 md:py-32 bg-surface/40 border-y border-white/5">
      <div className="max-w-7xl mx-auto px-6 grid lg:grid-cols-2 gap-16 items-center">
        <div className="order-2 lg:order-1">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Why Homeowners Choose Us</div>
          <h2 className="font-serif text-4xl md:text-5xl leading-tight text-white mb-4">
            Comfort, quiet, and <span className="italic text-gold">measurable savings.</span>
          </h2>
          <p className="text-white/60 font-light text-lg mb-10">
            The right film transforms every room touched by direct sun — from grand great-rooms to primary suites facing the mountains.
          </p>

          <div className="grid grid-cols-2 gap-x-8 gap-y-10">
            {BENEFITS.map((b, i) => (
              <div key={b.label} data-testid={`benefit-${i}`}>
                <b.icon className="h-6 w-6 text-gold mb-3" strokeWidth={1.25} />
                <div className="font-serif text-3xl text-white">{b.stat}</div>
                <div className="text-gold text-xs uppercase tracking-widest mt-1">{b.label}</div>
                <p className="text-white/50 text-sm mt-2 font-light">{b.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="relative order-1 lg:order-2">
          <div className="absolute -inset-4 border border-gold/20" />
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img src={IMG} alt="Modern desert luxury home" className="relative w-full h-[520px] object-cover" />
        </div>
      </div>
    </section>
  );
}
