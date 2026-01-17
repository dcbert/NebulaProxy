import { ExternalLink, Maximize2 } from 'lucide-react';
import { Button } from '../ui/button';

export const ProxyViewer = ({ proxy }) => {
  if (!proxy) {
    return (
      <div className="flex-1 flex items-center justify-center p-4">
        <div className="text-center">
          <div className="mx-auto w-24 h-24 mb-6 rounded-full bg-gradient-to-br from-purple-500/20 to-blue-500/20 flex items-center justify-center">
            <Maximize2 className="h-12 w-12 text-purple-500" />
          </div>
          <h3 className="text-2xl font-semibold mb-2 text-foreground">No Proxy Selected</h3>
          <p className="text-muted-foreground">Select a proxy from the sidebar to view it here</p>
        </div>
      </div>
    );
  }

  return (
    <>
      {/* Desktop Header */}
      <div className="hidden md:flex border-b bg-card shadow-sm p-3 sm:p-4 flex-col sm:flex-row items-start sm:items-center justify-between gap-3">
        <div className="flex-1 min-w-0">
          <h2 className="text-lg sm:text-xl font-semibold truncate">{proxy.name}</h2>
          <p className="text-xs sm:text-sm text-muted-foreground mt-1 break-all">{proxy.target_url}</p>
        </div>
        <Button
          size="sm"
          variant="outline"
          onClick={() => window.open(`/proxy/${proxy.id}/`, '_blank')}
          className="gap-2 w-full sm:w-auto flex-shrink-0"
        >
          <ExternalLink className="h-4 w-4" />
          <span className="hidden sm:inline">Open in New Tab</span>
          <span className="sm:hidden">Open</span>
        </Button>
      </div>
      <div className="flex-1 overflow-hidden bg-background">
        <iframe
          key={proxy.id}
          src={`${window.location.origin}/proxy/${proxy.id}/`}
          className="w-full h-full border-0"
          title={proxy.name}
          sandbox="allow-same-origin allow-scripts allow-forms allow-popups allow-modals"
        />
      </div>
    </>
  );
};
