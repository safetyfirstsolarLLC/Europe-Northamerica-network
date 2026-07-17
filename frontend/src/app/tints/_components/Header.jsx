"use client";

import { useEffect, useState } from "react";
import { Menu, X } from "lucide-react";

const NAV = [
  { label: "Services", href: "#services" },
  { label: "Gallery", href: "#gallery" },
  { label: "Pricing", href: "#pricing" },
  { label: "Service Area", href: "#service-area" },
  { label: "FAQ", href: "#faq" },
];

export default function Header() {
  const [scrolled, setScrolled] = useState(false);
  const [open, setOpen] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener("scroll", onScroll);
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  return (
    <header
      data-testid="site-header"
      className={`fixed top-0 inset-x-0 z-40 transition-all ${
        scrolled ? "bg-[#0B0F15]/80 backdrop-blur-xl border-b border-white/10" : "bg-transparent"
      }`}
    >
      <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
        <a href="#top" data-testid="header-logo" className="flex items-center gap-3">
          <div className="h-9 w-9 border border-gold/60 flex items-center justify-center relative overflow-hidden">
            <div className="absolute inset-0 bg-gradient-to-br from-gold/30 to-transparent" />
            <span className="relative font-serif text-gold text-lg">M</span>
          </div>
          <div className="leading-tight">
            <div className="text-[10px] tracking-[0.3em] uppercase text-gold">Coachella Valley</div>
            <div className="font-serif text-white text-lg">Mobile Window Tinting</div>
          </div>
        </a>

        <nav className="hidden lg:flex items-center gap-10">
          {NAV.map((item) => (
            <a
              key={item.href}
              href={item.href}
              data-testid={`nav-link-${item.label.toLowerCase().replace(/\s/g, "-")}`}
              className="text-sm text-white/70 hover:text-gold gold-underline transition-colors"
            >
              {item.label}
            </a>
          ))}
        </nav>

        <a
          href="#quote"
          data-testid="header-cta-button"
          className="hidden lg:inline-block px-6 py-3 bg-gold hover:bg-gold-hover text-black text-xs uppercase tracking-widest transition-colors"
        >
          Free Quote
        </a>

        <button
          className="lg:hidden text-white"
          onClick={() => setOpen(!open)}
          data-testid="mobile-menu-toggle"
          aria-label="Toggle menu"
        >
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {open && (
        <div className="lg:hidden bg-[#0B0F15] border-t border-white/10 px-6 py-6" data-testid="mobile-menu">
          <div className="flex flex-col gap-5">
            {NAV.map((item) => (
              <a
                key={item.href}
                href={item.href}
                className="text-white/80 hover:text-gold"
                onClick={() => setOpen(false)}
              >
                {item.label}
              </a>
            ))}
            <a
              href="#quote"
              onClick={() => setOpen(false)}
              className="mt-2 inline-block px-6 py-3 bg-gold text-black text-xs uppercase tracking-widest text-center"
            >
              Free Quote
            </a>
          </div>
        </div>
      )}
    </header>
  );
}
