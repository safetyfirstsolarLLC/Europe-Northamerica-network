import Link from "next/link";
import { Phone, Mail, MapPin } from "lucide-react";

const FOOTER_IMG = "https://images.unsplash.com/photo-1457725798811-c9561232a295?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxkZXNlcnQlMjBzdW5zZXQlMjBwYWxtJTIwdHJlZXN8ZW58MHx8fHwxNzgzMTA4ODg3fDA&ixlib=rb-4.1.0&q=85";

export default function Footer() {
  return (
    <footer data-testid="site-footer" className="relative overflow-hidden">
      <div className="absolute inset-0">
        {/* eslint-disable-next-line @next/next/no-img-element */}
        <img src={FOOTER_IMG} alt="Desert sunset" className="w-full h-full object-cover" />
        <div className="absolute inset-0 bg-[#0B0F15]/90" />
      </div>

      <div className="relative max-w-7xl mx-auto px-6 py-24">
        <div className="grid md:grid-cols-4 gap-12">
          <div className="md:col-span-2">
            <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Contact</div>
            <h3 className="font-serif text-4xl md:text-5xl text-white leading-tight">
              Ready when you are.<br />
              <span className="italic text-gold">Let&apos;s talk windows.</span>
            </h3>
            <p className="mt-6 text-white/60 max-w-md font-light">
              Reach us directly — text, call, or email. We respond within business hours across the Coachella Valley.
            </p>
          </div>

          <div>
            <div className="text-[10px] tracking-[0.3em] uppercase text-gold mb-4">Direct</div>
            <ul className="space-y-4 text-white/80">
              <li className="flex items-start gap-3">
                <Phone className="h-4 w-4 text-gold mt-1" strokeWidth={1.5} />
                <a href="tel:+17606411230" data-testid="footer-phone" className="gold-underline">(760) 641-1230</a>
              </li>
              <li className="flex items-start gap-3">
                <Mail className="h-4 w-4 text-gold mt-1" strokeWidth={1.5} />
                <a href="mailto:1piraspberry0.0.01@gmail.com" data-testid="footer-email" className="gold-underline text-sm break-all">
                  1piraspberry0.0.01@gmail.com
                </a>
              </li>
              <li className="flex items-start gap-3">
                <MapPin className="h-4 w-4 text-gold mt-1" strokeWidth={1.5} />
                <span>Mobile service · Coachella Valley &amp; Morongo Basin</span>
              </li>
            </ul>
          </div>

          <div>
            <div className="text-[10px] tracking-[0.3em] uppercase text-gold mb-4">Hours</div>
            <ul className="space-y-2 text-white/80 text-sm">
              <li className="flex justify-between"><span>Mon – Fri</span><span className="text-white/50">7am – 6pm</span></li>
              <li className="flex justify-between"><span>Saturday</span><span className="text-white/50">8am – 4pm</span></li>
              <li className="flex justify-between"><span>Sunday</span><span className="text-white/50">By appt.</span></li>
            </ul>
          </div>
        </div>

        <div className="mt-20 pt-8 border-t border-white/10 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
          <div className="text-white/40 text-xs">
            © {new Date().getFullYear()} Mobile Window Tinting. Licensed &amp; insured. Serving Coachella Valley.
          </div>
          <Link href="/tints/admin" data-testid="footer-admin-link" className="text-white/30 hover:text-gold text-xs uppercase tracking-widest">
            Admin
          </Link>
        </div>
      </div>
    </footer>
  );
}
