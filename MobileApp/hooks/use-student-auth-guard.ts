import AsyncStorage from "@react-native-async-storage/async-storage";
import { usePathname, useRouter } from "expo-router";
import { useEffect, useState } from "react";

const PUBLIC_PATHS = new Set([
  "/",
  "/loginform",
  "/register",
  "/dashboard",
  "/welcome",
  "/public-overview",
  "/app",
]);

export function useStudentAuthGuard() {
  const router = useRouter();
  const pathname = usePathname();
  const [ready, setReady] = useState(false);

  useEffect(() => {
    let cancelled = false;

    const verify = async () => {
      if (PUBLIC_PATHS.has(pathname)) {
        if (!cancelled) setReady(true);
        return;
      }

      const token = await AsyncStorage.getItem("access_token");
      if (!token) {
        router.replace("/loginform" as any);
        return;
      }

      if (!cancelled) setReady(true);
    };

    verify();
    return () => {
      cancelled = true;
    };
  }, [pathname, router]);

  return ready;
}
