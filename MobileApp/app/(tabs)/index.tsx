import AsyncStorage from "@react-native-async-storage/async-storage";
import { Redirect, useRouter } from "expo-router";
import { useEffect, useState } from "react";
import { ActivityIndicator, View } from "react-native";

export default function Index() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      const token = await AsyncStorage.getItem("access_token");
      const guestSession = await AsyncStorage.getItem("guest_session");
      router.replace((token || guestSession ? "/dashboard" : "/loginform") as any);
      setChecking(false);
    };

    checkSession();
  }, [router]);

  if (checking) {
    return (
      <View style={{ flex: 1, alignItems: "center", justifyContent: "center", backgroundColor: "#F6F3FF" }}>
        <ActivityIndicator size="large" color="#5523D2" />
      </View>
    );
  }

  return <Redirect href="/loginform" />;
}
