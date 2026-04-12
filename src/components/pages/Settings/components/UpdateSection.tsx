import { Sparkles, ExternalLink, Check, AlertCircle } from "lucide-react";
import {
  Item,
  ItemContent,
  ItemTitle,
  ItemDescription,
  ItemActions,
} from "@/components/ui/item";
import type { UpdateInfo } from "@/services/update";

interface UpdateSectionProps {
  checkingUpdate: boolean;
  currentVersion: string;
  onCheckUpdate: () => void;
  updateInfo: UpdateInfo | null;
  onOpenDownload: (url: string) => void;
}

export function UpdateSection({
  checkingUpdate,
  currentVersion,
  onCheckUpdate,
  updateInfo,
  onOpenDownload,
}: UpdateSectionProps) {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("zh-CN", {
      year: "numeric",
      month: "long",
      day: "numeric",
    });
  };

  return (
    <div className="space-y-3">
      <div className="flex items-center gap-2 text-sm font-medium text-foreground">
        <Sparkles className="w-4 h-4" />
        <span>更新</span>
      </div>
      <div className="rounded-lg bg-card overflow-hidden">
        <Item
          variant="outline"
          className="border-0 border-b border-border/60 last:border-0"
        >
          <ItemContent>
            <ItemTitle>应用更新</ItemTitle>
            <ItemDescription className="text-xs">
              {currentVersion && (
                <span>当前版本: v{currentVersion}</span>
              )}
            </ItemDescription>
          </ItemContent>
          <ItemActions>
            <button
              onClick={onCheckUpdate}
              disabled={checkingUpdate}
              className={`px-3 py-1.5 text-xs rounded transition-colors ${
                checkingUpdate
                  ? "bg-muted text-muted-foreground cursor-not-allowed"
                  : "bg-foreground text-background hover:opacity-90"
              }`}
            >
              {checkingUpdate ? "检查中..." : "检测更新"}
            </button>
          </ItemActions>
        </Item>

        {updateInfo && (
          <Item variant="outline" className="border-0 border-b border-border/60">
            <ItemContent>
              <div className="flex items-center gap-2">
                {updateInfo.hasUpdate ? (
                  <>
                    <AlertCircle className="w-4 h-4 text-yellow-500" />
                    <ItemTitle className="text-yellow-500">发现新版本</ItemTitle>
                  </>
                ) : (
                  <>
                    <Check className="w-4 h-4 text-green-500" />
                    <ItemTitle className="text-green-500">已是最新版本</ItemTitle>
                  </>
                )}
              </div>
              <ItemDescription className="text-xs">
                {updateInfo.hasUpdate ? (
                  <span>
                    最新版本: v{updateInfo.latestVersion}
                    {updateInfo.publishedAt && (
                      <span className="ml-2 text-muted-foreground">
                        ({formatDate(updateInfo.publishedAt)})
                      </span>
                    )}
                  </span>
                ) : (
                  <span>v{updateInfo.latestVersion}</span>
                )}
              </ItemDescription>
            </ItemContent>
            {updateInfo.hasUpdate && updateInfo.downloadUrl && (
              <ItemActions>
                <button
                  onClick={() => onOpenDownload(updateInfo.downloadUrl)}
                  className="flex items-center gap-1 px-3 py-1.5 text-xs rounded bg-primary text-primary-foreground hover:opacity-90 transition-colors"
                >
                  <ExternalLink className="w-3 h-3" />
                  下载更新
                </button>
              </ItemActions>
            )}
          </Item>
        )}
      </div>
    </div>
  );
}
