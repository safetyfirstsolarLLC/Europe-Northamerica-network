const IMGS = [
  { src: "https://images.unsplash.com/photo-1590912550141-1448da2bd5da?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODd8MHwxfHNlYXJjaHwyfHxtb2Rlcm4lMjBkZXNlcnQlMjBsdXh1cnklMjBob21lJTIwZXh0ZXJpb3IlMjBwYWxtJTIwc3ByaW5nc3xlbnwwfHx8fDE3ODMxMDg4ODd8MA&ixlib=rb-4.1.0&q=85", tag: "Palm Desert · Mid-century Estate" },
  { src: "https://images.unsplash.com/photo-1709418354364-8f3e9ad5c32c?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NTYxODd8MHwxfHNlYXJjaHwxfHxtb2Rlcm4lMjBkZXNlcnQlMjBsdXh1cnklMjBob21lJTIwZXh0ZXJpb3IlMjBwYWxtJTIwc3ByaW5nc3xlbnwwfHx8fDE3ODMxMDg4ODd8MA&ixlib=rb-4.1.0&q=85", tag: "Palm Springs · Contemporary" },
  { src: "https://images.unsplash.com/photo-1696986324679-dad26261d579?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NTY2NzV8MHwxfHNlYXJjaHwyfHxzdW5ueSUyMGxpdmluZyUyMHJvb20lMjBsYXJnZSUyMHdpbmRvd3MlMjBsdXh1cnl8ZW58MHx8fHwxNzgzMTA4ODg3fDA&ixlib=rb-4.1.0&q=85", tag: "La Quinta · Great Room" },
  { src: "https://images.unsplash.com/photo-1457725798811-c9561232a295?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDk1ODF8MHwxfHNlYXJjaHwxfHxkZXNlcnQlMjBzdW5zZXQlMjBwYWxtJTIwdHJlZXN8ZW58MHx8fHwxNzgzMTA4ODg3fDA&ixlib=rb-4.1.0&q=85", tag: "Rancho Mirage · Poolside" },
];

export default function Gallery() {
  return (
    <section id="gallery" data-testid="gallery-section" className="py-24 md:py-32">
      <div className="max-w-7xl mx-auto px-6">
        <div className="flex items-end justify-between mb-14">
          <div>
            <div className="text-[11px] tracking-[0.4em] uppercase text-gold mb-4">Selected Work</div>
            <h2 className="font-serif text-4xl md:text-5xl text-white">Recent installations.</h2>
          </div>
          <p className="hidden md:block max-w-md text-white/50 text-sm font-light">
            A discreet look at homes we've served across the valley. Full portfolio available on request.
          </p>
        </div>

        <div className="grid md:grid-cols-2 gap-6">
          {IMGS.map((img, i) => (
            <figure
              key={i}
              data-testid={`gallery-item-${i}`}
              className={`group relative overflow-hidden ${i % 3 === 0 ? "md:row-span-2" : ""}`}
            >
              {/* eslint-disable-next-line @next/next/no-img-element */}
              <img
                src={img.src}
                alt={img.tag}
                className={`w-full object-cover transition-transform duration-700 group-hover:scale-105 ${i % 3 === 0 ? "h-[540px] md:h-full" : "h-80"}`}
              />
              <div className="absolute inset-0 bg-gradient-to-t from-[#0B0F15]/90 via-transparent to-transparent" />
              <figcaption className="absolute bottom-6 left-6 right-6">
                <div className="text-[10px] uppercase tracking-[0.3em] text-gold">Case Study</div>
                <div className="font-serif text-xl text-white mt-1">{img.tag}</div>
              </figcaption>
            </figure>
          ))}
        </div>
      </div>
    </section>
  );
}
