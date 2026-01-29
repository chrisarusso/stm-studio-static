// @ts-check
import { defineConfig } from 'astro/config';

// https://astro.build/config
export default defineConfig({
  site: 'https://stm.studio',
  output: 'static',
  build: {
    // Generate clean URLs without .html extension
    format: 'directory'
  }
});
