import { ArrowRight, Sun } from "lucide-react";

const HERO_IMG =
  "https://images.unsplash.com/photo-1696986324679-dad26261d579?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxzdW5ueSUyMGxpdmluZyUyMHJvb20lMjBsYXJnZSUyMHdpbmRvd3MlMjBsdXh1cnl8ZW58MHx8fHwxNzgzMTA4ODg3fDA&ixlib=rb-4.1.0&q=85";

export default function Hero() {
  return (
    <section id="top" data-testid="hero-section" className="relative min-h-screen flex items-end overflow-hidden">
      <div className="absolute inset-0">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={HERO_IMG} alt="Luxury living room with panoramic windows" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-gradient-to-b from-[#0B0F15]/60 via-[#0B0F15]/70 to-[#0B0F15]" />
        <div className="absolute inset-0 grain-overlay" />
      </div>

      <div className="relative max-w-7xl mx-auto px-6 py-24 md:py-32 w-full">
        <div className="max-w-3xl animate-fade-up">
          <div className="flex items-center gap-3 mb-8">
            <div className="h-px w-12 bg-gold" />
            <span className="text-[11px] tracking-[0.4em] uppercase text-gold flex items-center gap-2">
              <Sun className="h-3.5 w-3.5" strokeWidth={1.5} /> Coachella Valley · Est. Mobile Service
            </span>
          </div>

          <h1 className="font-serif text-5xl sm:text-6xl lg:text-7xl leading-[1.02] tracking-tight text-white">
            The desert sun
            <br />
            <span className="italic text-gold">tamed</span> at your window.
          </h1>

          <p className="mt-8 text-lg text-white/70 max-w-xl font-light leading-relaxed">
            Precision solar window tinting for high-end estates across Palm Springs,
            Palm Desert, Coachella, Twentynine Palms and Joshua Tree. We come to you.
          </p>

          <div className="mt-10 flex flex-col sm:flex-row items-start sm:items-center gap-4">
            <a
              href="#quote"
              data-testid="hero-quote-button"
              className="group inline-flex items-center gap-3 px-8 py-4 bg-gold hover:bg-gold-hover text-black text-xs uppercase tracking-[0.25em] transition-colors"
            >
              Request Private Estimate
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" strokeWidth={1.5} />
            </a>
            <a
              href="tel:+17606411230"
              data-testid="hero-phone-link"
              className="text-white/80 hover:text-gold text-sm tracking-wide gold-underline"
            >
              or call (760) 641-1230
            </a>
          </div>

          <div className="mt-16 grid grid-cols-3 max-w-lg gap-8 border-t border-white/10 pt-8">
            <Stat value="99%" label="UV Blocked" />
            <Stat value="82°F" label="Cooler Glass" />
            <Stat value="15yr" label="Warranty" />
          </div>
        </div>
      </div>
    </section>
  );
}

const Stat = ({ value, label }) => (
  <div>
    <div className="font-serif text-3xl text-gold">{value}</div>
    <div className="text-[10px] uppercase tracking-[0.3em] text-white/50 mt-1">{label}</div>
  </div>
);
