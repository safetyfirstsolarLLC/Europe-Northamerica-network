import { Check } from "lucide-react";

const TIERS = [
  {
    name: "Essential",
    tagline: "Sun-facing rooms",
    price: "From $6",
    unit: "/ sq ft",
    features: [
      "Solar heat-rejection film",
      "99% UV protection",
      "Standard clear or light-tint options",
      "10-year residential warranty",
      "Professional mobile install",
    ],
  },
  {
    name: "Signature",
    tagline: "Full-home comfort",
    price: "From $11",
    unit: "/ sq ft",
    features: [
      "Ceramic nano film",
      "78% infrared rejection",
      "Preserves natural light & views",
      "15-year warranty (lifetime residential)",
      "Free consultation & sample kit",
    ],
    featured: true,
  },
  {
    name: "Estate",
    tagline: "Turnkey luxury",
    price: "Custom",
    unit: "quote",
    features: [
      "Spectrally selective premium film",
      "Custom privacy & decorative films",
      "Dedicated project manager",
      "Lifetime warranty",
      "White-glove concierge service",
    ],
  },
];

export default function Pricing() {
  return (
    <section id="pricing" data-testid="pricing-section" className="py-24 md:py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="max-w-2xl mb-16">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Investment</div>
          <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight">
            Three tiers, priced <span className="italic text-gold">honestly</span>.
          </h2>
          <p className="mt-4 text-white/60 font-light text-lg">
            Every quote is built from your specific window count and orientation. Prices below are per-square-foot starting points, all-inclusive of premium film and expert installation.
          </p>
        </div>

        <div className="grid md:grid-cols-3 gap-0 border border-white/10">
          {TIERS.map((t) => (
            <div
              key={t.name}
              data-testid={`pricing-tier-${t.name.toLowerCase()}`}
              className={`p-10 border-r border-white/10 last:border-r-0 ${t.featured ? "bg-gold/5 relative" : ""}`}
            >
              {t.featured && (
                <div className="absolute top-0 right-0 bg-gold text-black text-[10px] uppercase tracking-[0.25em] px-3 py-1">
                  Most Chosen
                </div>
              )}
              <div className="text-[11px] uppercase tracking-[0.3em] text-gold">{t.tagline}</div>
              <h3 className="font-serif text-3xl mt-3 text-white">{t.name}</h3>
              <div className="mt-6 flex items-baseline gap-2">
                <span className="font-serif text-4xl text-white">{t.price}</span>
                <span className="text-white/50 text-sm">{t.unit}</span>
              </div>
              <ul className="mt-8 space-y-3">
                {t.features.map((f) => (
                  <li key={f} className="flex items-start gap-3 text-white/80 text-sm font-light">
                    <Check className="h-4 w-4 text-gold mt-0.5 flex-shrink-0" strokeWidth={1.5} />
                    <span>{f}</span>
                  </li>
                ))}
              </ul>
              <a
                href="#quote"
                data-testid={`pricing-cta-${t.name.toLowerCase()}`}
                className={`mt-8 inline-block w-full text-center px-6 py-3 text-xs uppercase tracking-widest transition-colors ${
                  t.featured
                    ? "bg-gold hover:bg-gold-hover text-black"
                    : "border border-white/20 text-white hover:border-gold hover:text-gold"
                }`}
              >
                Request quote
              </a>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
