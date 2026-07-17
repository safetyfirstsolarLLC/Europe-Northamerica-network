import { Quote } from "lucide-react";

const REVIEWS = [
  {
    text: "The great room went from unusable in the afternoon to our favorite spot. You cannot tell there's film on the glass unless you look for it.",
    name: "Andrea M.",
    place: "Rancho Mirage",
  },
  {
    text: "They arrived on time, protected everything, worked quietly, and the crew was in and out in one day. Best mobile service we've hired in the valley.",
    name: "David & Kim S.",
    place: "Palm Desert",
  },
  {
    text: "Our art collection was fading. Now it's protected and the AC bill dropped noticeably in July. Only wish we'd done this five summers ago.",
    name: "Renata C.",
    place: "La Quinta",
  },
];

export default function Testimonials() {
  return (
    <section data-testid="testimonials-section" className="py-24 md:py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Homeowner Voices</div>
        <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight mb-14">
          Quiet reviews from <span className="italic text-gold">discerning clients.</span>
        </h2>

        <div className="grid md:grid-cols-3 gap-6">
          {REVIEWS.map((r, i) => (
            <figure
              key={i}
              data-testid={`testimonial-${i}`}
              className="bg-surface border border-white/10 p-8 flex flex-col"
            >
              <Quote className="h-8 w-8 text-gold mb-6" strokeWidth={1} />
              <blockquote className="font-serif text-lg text-white/90 leading-relaxed flex-grow italic">
                &ldquo;{r.text}&rdquo;
              </blockquote>
              <figcaption className="mt-6 pt-6 border-t border-white/10">
                <div className="text-white">{r.name}</div>
                <div className="text-gold text-xs uppercase tracking-widest mt-1">{r.place}</div>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
