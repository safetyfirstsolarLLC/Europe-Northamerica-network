"use client";

import Header from "./Header";
import Hero from "./Hero";
import Services from "./Services";
import Benefits from "./Benefits";
import Gallery from "./Gallery";
import Pricing from "./Pricing";
import ServiceArea from "./ServiceArea";
import Testimonials from "./Testimonials";
import QuoteForm from "./QuoteForm";
import FAQ from "./FAQ";
import Footer from "./Footer";

export default function LandingPage() {
  return (
    <div data-testid="landing-page" className="relative">
      <Header />
      <main>
        <Hero />
        <Services />
        <Benefits />
        <Gallery />
        <Pricing />
        <ServiceArea />
        <Testimonials />
        <QuoteForm />
        <FAQ />
      </main>
      <Footer />
    </div>
  );
}
