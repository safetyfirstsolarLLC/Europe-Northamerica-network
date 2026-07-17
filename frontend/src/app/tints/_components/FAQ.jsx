import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";

const FAQS = [
  { q: "How long does an average install take?", a: "Most homes are completed in a single day. Larger estates may require two days. We arrive with drop cloths and protect all surfaces before starting." },
  { q: "Will the film change the look of my windows?", a: "Modern ceramic and spectrally-selective films are nearly invisible. From the interior, views are preserved. From the exterior, the glass has a subtle, uniform tone." },
  { q: "Is this safe for dual-pane and low-e windows?", a: "Yes — we specifically select films rated for the type of glazing in your home to avoid seal failure or thermal stress. We inspect every window before quoting." },
  { q: "How much can I really save on cooling?", a: "Coachella Valley homes typically see 20–35% reduction in cooling cost during summer months, along with improved comfort throughout." },
  { q: "Do you offer any warranty?", a: "Yes. Every install includes a manufacturer warranty of 10–15 years, with lifetime residential coverage on our Signature and Estate films." },
  { q: "Do you service commercial or HOA projects?", a: "Yes. Please mention your project scope in the quote form and we'll route you to the right specialist." },
];

export default function FAQ() {
  return (
    <section id="faq" data-testid="faq-section" className="py-24 md:py-32">
      <div className="max-w-4xl mx-auto px-6">
        <div className="text-center mb-14">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Questions</div>
          <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight">Frequently asked.</h2>
        </div>
        <Accordion type="single" collapsible className="border-t border-white/10">
          {FAQS.map((f, i) => (
            <AccordionItem key={i} value={`item-${i}`} data-testid={`faq-item-${i}`} className="border-b border-white/10">
              <AccordionTrigger className="text-left font-serif text-xl text-white hover:text-gold py-6 hover:no-underline">
                {f.q}
              </AccordionTrigger>
              <AccordionContent className="text-white/60 font-light leading-relaxed pb-6 text-base">
                {f.a}
              </AccordionContent>
            </AccordionItem>
          ))}
        </Accordion>
      </div>
    </section>
  );
}
