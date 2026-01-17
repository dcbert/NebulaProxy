import { Activity, Globe, Trash2 } from 'lucide-react';
import { cn } from '../../lib/utils';
import { Button } from '../ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '../ui/card';

export const ProxyCard = ({ proxy, selected, onClick, onDelete }) => {
  return (
    <Card
      className={cn(
        "cursor-pointer transition-all hover:shadow-lg hover:scale-[1.02] group",
        selected ? 'ring-2 ring-purple-500 shadow-lg shadow-purple-500/20' : 'hover:ring-1 hover:ring-purple-300'
      )}
      onClick={onClick}
    >
      <CardHeader className="pb-3">
        <div className="flex items-start justify-between">
          <div className="flex-1 min-w-0">
            <CardTitle className="text-base sm:text-lg flex items-center gap-2 truncate">
              <Globe className="h-4 w-4 text-purple-500 flex-shrink-0" />
              <span className="truncate">{proxy.name}</span>
            </CardTitle>
            {proxy.description && (
              <CardDescription className="mt-1.5 text-xs line-clamp-2">
                {proxy.description}
              </CardDescription>
            )}
          </div>
          <Button
            size="sm"
            variant="ghost"
            className="text-red-500 hover:text-red-600 hover:bg-red-500/10 ml-2 flex-shrink-0"
            onClick={(e) => {
              e.stopPropagation();
              if (window.confirm(`Delete "${proxy.name}"?`)) {
                onDelete(proxy.id);
              }
            }}
          >
            <Trash2 className="h-4 w-4" />
          </Button>
        </div>
      </CardHeader>
      <CardContent className="pb-3">
        <div className="flex items-center gap-2 text-xs text-muted-foreground">
          <Activity className="h-3 w-3 flex-shrink-0" />
          <span className="break-all">{proxy.target_url}</span>
        </div>
      </CardContent>
    </Card>
  );
};
