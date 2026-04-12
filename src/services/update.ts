import { getName, getVersion } from "@tauri-apps/api/app";

const GITHUB_REPO = "zhengddzz/ChmlFrp-NodeSpeedTest";
const GITHUB_API_URL = `https://api.github.com/repos/${GITHUB_REPO}/releases/latest`;

export interface UpdateInfo {
  hasUpdate: boolean;
  currentVersion: string;
  latestVersion: string;
  downloadUrl: string;
  releaseNotes: string;
  publishedAt: string;
}

export async function getCurrentVersion(): Promise<string> {
  try {
    const version = await getVersion();
    return version;
  } catch {
    return "1.0.0";
  }
}

export async function getAppName(): Promise<string> {
  try {
    const name = await getName();
    return name;
  } catch {
    return "ChmlFrp节点推荐器";
  }
}

export async function checkForUpdates(): Promise<UpdateInfo | null> {
  try {
    const currentVersion = await getCurrentVersion();

    const response = await fetch(GITHUB_API_URL, {
      headers: {
        Accept: "application/vnd.github.v3+json",
      },
    });

    if (!response.ok) {
      if (response.status === 404) {
        return null;
      }
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const release = await response.json();
    const latestVersion = release.tag_name.replace(/^v/, "");

    const compareVersions = (current: string, latest: string): boolean => {
      const currentParts = current.split(".").map(Number);
      const latestParts = latest.split(".").map(Number);

      for (let i = 0; i < Math.max(currentParts.length, latestParts.length); i++) {
        const currentPart = currentParts[i] || 0;
        const latestPart = latestParts[i] || 0;

        if (latestPart > currentPart) return true;
        if (latestPart < currentPart) return false;
      }

      return false;
    };

    const hasUpdate = compareVersions(currentVersion, latestVersion);

    let downloadUrl = "";
    const platform = navigator.platform.toLowerCase();

    if (platform.includes("win")) {
      const msiAsset = release.assets.find(
        (a: { name: string }) => a.name.endsWith(".msi")
      );
      const exeAsset = release.assets.find(
        (a: { name: string }) => a.name.endsWith(".exe") && !a.name.includes("nsis")
      );
      downloadUrl = msiAsset?.browser_download_url || exeAsset?.browser_download_url || "";
    } else if (platform.includes("mac")) {
      const dmgAsset = release.assets.find(
        (a: { name: string }) => a.name.endsWith(".dmg")
      );
      downloadUrl = dmgAsset?.browser_download_url || "";
    } else if (platform.includes("linux")) {
      const debAsset = release.assets.find(
        (a: { name: string }) => a.name.endsWith(".deb")
      );
      const appImageAsset = release.assets.find(
        (a: { name: string }) => a.name.endsWith(".AppImage")
      );
      downloadUrl = debAsset?.browser_download_url || appImageAsset?.browser_download_url || "";
    }

    if (!downloadUrl && release.assets.length > 0) {
      downloadUrl = release.html_url;
    }

    return {
      hasUpdate,
      currentVersion,
      latestVersion,
      downloadUrl,
      releaseNotes: release.body || "",
      publishedAt: release.published_at,
    };
  } catch (error) {
    console.error("Failed to check for updates:", error);
    return null;
  }
}

export function openDownloadPage(url: string): void {
  window.open(url, "_blank");
}
