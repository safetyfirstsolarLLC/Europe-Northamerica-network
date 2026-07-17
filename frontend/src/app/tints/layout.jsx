import Providers from "./_components/Providers";
import "./tints.css";

export const metadata = {
  title: "Mobile Window Tinting — Luxury Solar Window Tint | Coachella Valley",
  description:
    "Premium mobile solar window tinting for high-end homes in Palm Springs, Palm Desert, Coachella, 29 Palms, and Joshua Tree.",
};

/**
 * Segment layout for /tints.
 * `.tints-root` scopes the luxury dark theme CSS variables so it does not
 * leak into the rest of your site.
 */
export default function TintsLayout({ children }) {
  return (
    <div className="tints-root min-h-screen bg-background text-foreground">
      <Providers>{children}</Providers>
    </div>
  );
}
