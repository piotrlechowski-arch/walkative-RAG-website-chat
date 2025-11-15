
import React from 'react';
import type { Source } from '../types';
import { LinkIcon } from './icons/LinkIcon';

interface SourceCardProps {
  source: Source;
}

const SourceCard: React.FC<SourceCardProps> = ({ source }) => {
  return (
    <a
      href={source.url}
      target="_blank"
      rel="noopener noreferrer"
      className="block bg-gray-700/50 hover:bg-gray-700 border border-gray-600 p-3 rounded-lg transition-all duration-200 group"
    >
      <div className="flex items-center space-x-2">
        <LinkIcon className="w-4 h-4 text-gray-400 group-hover:text-cyan-400 transition-colors" />
        <h5 className="text-sm font-semibold text-gray-200 truncate group-hover:text-cyan-400 transition-colors">{source.title}</h5>
      </div>
      <p className="text-xs text-gray-400 mt-1 line-clamp-2">
        {source.snippet}
      </p>
    </a>
  );
};

export default SourceCard;
