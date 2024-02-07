import path from "path";
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

export const outDir = path.resolve(__dirname, 'dist');
export const imagesDir = path.resolve(__dirname, 'src', 'assets', 'images');
export const entry = './src/index.tsx';
