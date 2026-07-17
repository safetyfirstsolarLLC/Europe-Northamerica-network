import { Sun, ShieldCheck, Eye, Sparkles, Thermometer, Leaf } from "lucide-react";

const SERVICES = [
  { icon: Thermometer, title: "Heat Rejection Films", desc: "Rejects up to 78% of solar heat. Feel the room cool the moment installation is complete." },
  { icon: Sun, title: "Spectrally Selective", desc: "Crystal-clear films that block infrared without sacrificing natural desert light." },
  { icon: ShieldCheck, title: "99% UV Protection", desc: "Protect flooring, art, and furnishings from Coachella Valley's relentless UV exposure." },
  { icon: Eye, title: "Privacy & Frost Films", desc: "Boutique privacy solutions — one-way mirror, gradient frost, decorative etched glass." },
  { icon: Sparkles, title: "Ceramic Nano Films", desc: "Top-tier automotive-grade ceramics adapted for premium residential glazing." },
  { icon: Leaf, title: "Low-E Retrofit", desc: "Improve energy performance of existing windows without full replacement." },
];

export default function Services() {
  return (
    <section id="services" data-testid="services-section" className="py-24 md:py-32 relative">
      <div className="max-w-7xl mx-auto px-6">
        <div className="max-w-2xl mb-16">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Our Craft</div>
          <h2 className="font-serif text-4xl md:text-5xl leading-tight text-white">
            Solar window films <span className="italic text-gold">engineered</span> for desert living.
          </h2>
          <p className="mt-6 text-white/60 text-lg font-light">
            Every product we install is selected for the Coachella Valley climate — brutal sun, low humidity, and homeowners who expect flawless craftsmanship.
          </p>
        </div>

        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {SERVICES.map((s, i) => (
            <div
              key={s.title}
              data-testid={`service-card-${i}`}
              className="group bg-surface border border-white/10 p-8 hover:border-gold/40 hover:-translate-y-1 transition-all"
            >
              <s.icon className="h-8 w-8 text-gold mb-6" strokeWidth={1.25} />
              <h3 className="font-serif text-2xl text-white mb-3">{s.title}</h3>
              <p className="text-white/60 font-light leading-relaxed">{s.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
