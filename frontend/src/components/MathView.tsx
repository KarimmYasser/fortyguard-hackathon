import React, { useMemo } from 'react';
import katex from 'katex';
// Co-located with the only consumer of KaTeX so the stylesheet ships in the
// lazy math chunk rather than the render-blocking entry CSS.
import 'katex/dist/katex.min.css';

interface MathViewProps {
  math: string;
  displayMode?: boolean;
  className?: string;
  scale?: 'sm' | 'md' | 'lg' | 'auto';
}

export const MathView: React.FC<MathViewProps> = ({
  math,
  displayMode = true,
  className = '',
  scale = 'auto',
}) => {
  const html = useMemo(() => {
    try {
      return katex.renderToString(math, {
        displayMode,
        throwOnError: false,
      });
    } catch (e) {
      console.warn('KaTeX render error for formula:', math, e);
      return math;
    }
  }, [math, displayMode]);

  const scaleClasses =
    scale === 'sm'
      ? 'text-[11px] sm:text-xs'
      : scale === 'md'
      ? 'text-xs sm:text-sm'
      : scale === 'lg'
      ? 'text-sm sm:text-base'
      : 'text-[11px] sm:text-xs md:text-[12.5px]';

  return (
    <span
      className={`katex-math-container font-serif text-slate-100 max-w-full overflow-hidden inline-flex items-center justify-center leading-tight ${scaleClasses} ${className}`}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
};
