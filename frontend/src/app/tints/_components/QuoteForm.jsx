"use client";

import { useState } from "react";
import { api } from "../_lib/api";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { toast } from "sonner";
import { CalendarIcon, Send, CheckCircle2 } from "lucide-react";
import { format } from "date-fns";

const CITIES = ["Palm Springs", "Palm Desert", "Rancho Mirage", "La Quinta", "Indian Wells", "Coachella", "Twentynine Palms", "Joshua Tree", "Other"];
const HOME_SIZES = ["Under 2,000 sq ft", "2,000 – 3,500 sq ft", "3,500 – 5,000 sq ft", "5,000 – 8,000 sq ft", "Over 8,000 sq ft"];
const WINDOW_COUNTS = ["1 – 5", "6 – 15", "16 – 30", "31 – 50", "50+"];
const TINT_TYPES = ["Heat rejection (ceramic)", "Spectrally selective (clear)", "Privacy / mirror", "Decorative / frost", "Not sure — recommend for me"];

export default function QuoteForm() {
  const [form, setForm] = useState({
    name: "", email: "", phone: "", address: "",
    city: "", home_size: "", window_count: "", tint_type: "",
    preferred_date: null, message: "",
  });
  const [loading, setLoading] = useState(false);
  const [submitted, setSubmitted] = useState(false);

  const update = (k, v) => setForm((f) => ({ ...f, [k]: v }));

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await api.post("/leads", {
        ...form,
        preferred_date: form.preferred_date ? format(form.preferred_date, "yyyy-MM-dd") : null,
      });
      toast.success("Request received. We'll be in touch within 24 hours.");
      setSubmitted(true);
    } catch (err) {
      toast.error("Something went wrong. Please try again or call (760) 641-1230.");
    } finally {
      setLoading(false);
    }
  };

  if (submitted) {
    return (
      <section id="quote" data-testid="quote-form-section" className="py-24 md:py-32">
        <div className="max-w-3xl mx-auto px-6 text-center" data-testid="quote-success">
          <CheckCircle2 className="h-14 w-14 text-gold mx-auto mb-6" strokeWidth={1} />
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Received</div>
          <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight">Thank you — we&apos;ll be in touch shortly.</h2>
          <p className="mt-6 text-white/60 font-light text-lg">
            A specialist will call you within one business day to schedule your on-site consultation. In the meantime, feel free to reach us directly at <a href="tel:+17606411230" className="text-gold gold-underline">(760) 641-1230</a>.
          </p>
        </div>
      </section>
    );
  }

  return (
    <section id="quote" data-testid="quote-form-section" className="py-24 md:py-32 bg-surface/40 border-y border-white/5">
      <div className="max-w-5xl mx-auto px-6">
        <div className="text-center mb-14">
          <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Free Consultation</div>
          <h2 className="font-serif text-4xl md:text-5xl text-white leading-tight">
            Request a <span className="italic text-gold">private estimate.</span>
          </h2>
          <p className="mt-4 text-white/60 font-light">No obligation. On-site measurement and sample kit included.</p>
        </div>

        <form onSubmit={handleSubmit} className="bg-background border border-white/10 p-8 md:p-12 grid md:grid-cols-2 gap-6" data-testid="quote-form">
          <Field label="Full Name *" htmlFor="name">
            <Input required id="name" data-testid="quote-name-input" value={form.name} onChange={(e) => update("name", e.target.value)} className={inputCls} />
          </Field>
          <Field label="Email *" htmlFor="email">
            <Input required id="email" type="email" data-testid="quote-email-input" value={form.email} onChange={(e) => update("email", e.target.value)} className={inputCls} />
          </Field>
          <Field label="Phone *" htmlFor="phone">
            <Input required id="phone" data-testid="quote-phone-input" value={form.phone} onChange={(e) => update("phone", e.target.value)} className={inputCls} />
          </Field>
          <Field label="City / Area">
            <Select value={form.city} onValueChange={(v) => update("city", v)}>
              <SelectTrigger data-testid="quote-city-select" className={selectCls}><SelectValue placeholder="Select area" /></SelectTrigger>
              <SelectContent>{CITIES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </Field>
          <Field label="Property Address *" htmlFor="address" className="md:col-span-2">
            <Input required id="address" data-testid="quote-address-input" value={form.address} onChange={(e) => update("address", e.target.value)} className={inputCls} placeholder="Street address" />
          </Field>
          <Field label="Home Size">
            <Select value={form.home_size} onValueChange={(v) => update("home_size", v)}>
              <SelectTrigger data-testid="quote-home-size-select" className={selectCls}><SelectValue placeholder="Approx. size" /></SelectTrigger>
              <SelectContent>{HOME_SIZES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </Field>
          <Field label="Window Count">
            <Select value={form.window_count} onValueChange={(v) => update("window_count", v)}>
              <SelectTrigger data-testid="quote-window-count-select" className={selectCls}><SelectValue placeholder="Approx. windows" /></SelectTrigger>
              <SelectContent>{WINDOW_COUNTS.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </Field>
          <Field label="Tint Type Interest">
            <Select value={form.tint_type} onValueChange={(v) => update("tint_type", v)}>
              <SelectTrigger data-testid="quote-tint-type-select" className={selectCls}><SelectValue placeholder="Choose a film type" /></SelectTrigger>
              <SelectContent>{TINT_TYPES.map((c) => <SelectItem key={c} value={c}>{c}</SelectItem>)}</SelectContent>
            </Select>
          </Field>
          <Field label="Preferred Appointment Date">
            <Popover>
              <PopoverTrigger asChild>
                <button
                  type="button"
                  data-testid="quote-date-trigger"
                  className={`${selectCls} w-full flex items-center justify-between px-3`}
                >
                  <span className={form.preferred_date ? "text-white" : "text-white/40"}>
                    {form.preferred_date ? format(form.preferred_date, "PPP") : "Select a date"}
                  </span>
                  <CalendarIcon className="h-4 w-4 text-gold" />
                </button>
              </PopoverTrigger>
              <PopoverContent className="bg-surface border-white/10 p-0" align="start">
                <Calendar
                  mode="single"
                  selected={form.preferred_date}
                  onSelect={(d) => update("preferred_date", d)}
                  disabled={(d) => d < new Date(new Date().setHours(0, 0, 0, 0))}
                  initialFocus
                />
              </PopoverContent>
            </Popover>
          </Field>
          <Field label="Message / Anything specific?" htmlFor="message" className="md:col-span-2">
            <Textarea id="message" data-testid="quote-message-input" value={form.message} onChange={(e) => update("message", e.target.value)} rows={4} className="bg-transparent border-0 border-b border-white/20 rounded-none focus-visible:ring-0 focus-visible:border-gold px-0 py-3" />
          </Field>
          <div className="md:col-span-2 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pt-4">
            <p className="text-xs text-white/40 max-w-md">By submitting, you consent to a follow-up call. We never share your information.</p>
            <Button
              type="submit"
              disabled={loading}
              data-testid="quote-submit-button"
              className="rounded-none bg-gold hover:bg-gold-hover text-black uppercase tracking-widest text-xs px-10 py-6"
            >
              {loading ? "Sending…" : (<><Send className="h-4 w-4 mr-2" /> Submit Request</>)}
            </Button>
          </div>
        </form>
      </div>
    </section>
  );
}

const inputCls = "bg-transparent border-0 border-b border-white/20 rounded-none focus-visible:ring-0 focus-visible:border-gold px-0 h-11 text-white";
const selectCls = "bg-transparent border-0 border-b border-white/20 rounded-none focus:ring-0 h-11 text-white px-0";

const Field = ({ label, children, htmlFor, className = "" }) => (
  <div className={className}>
    <Label htmlFor={htmlFor} className="text-white/50 text-[11px] uppercase tracking-[0.25em]">{label}</Label>
    <div className="mt-1">{children}</div>
  </div>
);
