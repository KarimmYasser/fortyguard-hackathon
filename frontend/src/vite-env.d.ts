/// <reference types="vite/client" />

interface ImportMetaEnv {
  /** '1' when the pitch renders are bundled with the build (local dev only). */
  readonly VITE_PITCH_RENDER?: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
