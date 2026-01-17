import { AlertCircle, ExternalLink, Globe, Loader2, Menu } from 'lucide-react';
import { useState } from 'react';
import { AddProxyDialog } from '../components/proxy/AddProxyDialog';
import { ProxyCard } from '../components/proxy/ProxyCard';
import { ProxyViewer } from '../components/proxy/ProxyViewer';
import { Button } from '../components/ui/button';
import { useProxies } from '../hooks/useProxies';

export const Dashboard = () => {
  const { proxies, loading, error, addProxy, deleteProxy } = useProxies();
  const [selectedProxy, setSelectedProxy] = useState(null);
  const [showAddDialog, setShowAddDialog] = useState(false);
  const [sidebarOpen, setSidebarOpen] = useState(false);

  if (loading && proxies.length === 0) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-background">
        <div className="text-center">
          <Loader2 className="h-12 w-12 animate-spin text-purple-500 mx-auto mb-4" />
          <p className="text-muted-foreground">Loading proxies...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="h-screen flex bg-background">
      {/* Sidebar */}
      <div className={`
        fixed md:relative inset-y-0 left-0 z-40
        w-full sm:w-96 border-r border-border bg-card shadow-xl flex flex-col
        transform transition-transform duration-300 ease-in-out
        ${sidebarOpen ? 'translate-x-0' : '-translate-x-full md:translate-x-0'}
      `}>
        {/* Header */}
        <div className="p-4 sm:p-6 border-b border-border bg-gradient-to-br from-purple-600 via-blue-600 to-purple-700">
          <div className="flex items-center gap-3 mb-1">
            <div className="p-2 bg-white/10 rounded-lg backdrop-blur-sm">
              <Globe className="h-5 w-5 sm:h-6 sm:w-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl sm:text-2xl font-bold text-white">Reverse Proxy</h1>
              <p className="text-purple-100 text-xs sm:text-sm">Network Dashboard</p>
            </div>
          </div>
        </div>

        {/* Add Proxy Button */}
        <div className="p-3 sm:p-4 border-b border-border">
          <AddProxyDialog
            open={showAddDialog}
            onOpenChange={setShowAddDialog}
            onSubmit={addProxy}
          />
        </div>

        {/* Proxy List */}
        <div className="flex-1 overflow-y-auto p-3 sm:p-4 space-y-3">
          {error && (
            <div className="bg-destructive/10 border border-destructive/20 text-destructive p-3 rounded-lg text-sm flex items-center gap-2">
              <AlertCircle className="h-4 w-4 flex-shrink-0" />
              <span>{error}</span>
            </div>
          )}

          {proxies.length === 0 && !error && (
            <div className="text-center py-12">
              <div className="mx-auto w-16 h-16 mb-4 rounded-full bg-purple-500/10 flex items-center justify-center">
                <Globe className="h-8 w-8 text-purple-500/50" />
              </div>
              <p className="text-sm text-muted-foreground font-medium">No proxies configured</p>
              <p className="text-xs text-muted-foreground/70 mt-1">Click "Add New Proxy" to get started</p>
            </div>
          )}

          {proxies.map((proxy) => (
            <ProxyCard
              key={proxy.id}
              proxy={proxy}
              selected={selectedProxy?.id === proxy.id}
              onClick={() => {
                setSelectedProxy(proxy);
                setSidebarOpen(false);
              }}
              onDelete={(id) => {
                deleteProxy(id);
                if (selectedProxy?.id === id) {
                  setSelectedProxy(null);
                }
              }}
            />
          ))}
        </div>
      </div>

      {/* Overlay for mobile */}
      {sidebarOpen && (
        <div
          className="fixed inset-0 bg-black/50 z-30 md:hidden"
          onClick={() => setSidebarOpen(false)}
        />
      )}

      {/* Main Content */}
      <div className="flex-1 flex flex-col w-full md:w-auto">
        {/* Mobile Header with Menu Button */}
        {selectedProxy && (
          <div className="md:hidden border-b bg-card shadow-sm p-3 flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="flex-1 min-w-0">
              <h2 className="text-base font-semibold truncate">{selectedProxy.name}</h2>
            </div>
            <Button
              size="sm"
              variant="outline"
              onClick={() => window.open(`/proxy/${selectedProxy.id}/`, '_blank')}
            >
              <ExternalLink className="h-4 w-4" />
            </Button>
          </div>
        )}

        {!selectedProxy && (
          <div className="md:hidden border-b bg-card shadow-sm p-3 flex items-center gap-3">
            <Button
              variant="ghost"
              size="icon"
              onClick={() => setSidebarOpen(true)}
            >
              <Menu className="h-5 w-5" />
            </Button>
            <div className="flex-1">
              <h2 className="text-base font-semibold">Reverse Proxy</h2>
            </div>
          </div>
        )}

        <ProxyViewer proxy={selectedProxy} />
      </div>
    </div>
  );
};
