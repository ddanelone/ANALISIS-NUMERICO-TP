import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  devIndicators: false,
};

// para dockerizar paa
module.exports = {
  output: "standalone",
};

export default nextConfig;
