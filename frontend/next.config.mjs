/** @type {import('next').NextConfig} */
const nextConfig = {
  // Cloudflare Pages requires a static export structure for next-on-pages
  output: 'export',
  images: {
    unoptimized: true,
  },
};

export default nextConfig;
