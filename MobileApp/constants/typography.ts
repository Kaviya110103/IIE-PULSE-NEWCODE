import { Platform } from "react-native";

export const AppFont = {
  regular: Platform.select({
    web: "Calibri, Arial, system-ui, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
    default: "Calibri",
  }) as string,
};

export const Typography = {
  size: {
    caption: 10,
    meta: 11,
    small: 12,
    body: 13,
    bodyLarge: 14,
    subtitle: 16,
    title: 21,
    hero: 24,
  },
  lineHeight: {
    caption: 14,
    meta: 15,
    small: 17,
    body: 19,
    bodyLarge: 21,
    subtitle: 22,
    title: 27,
    hero: 30,
  },
};

export const defaultTextStyle = {
  fontFamily: AppFont.regular,
  fontSize: Typography.size.body,
  lineHeight: Typography.lineHeight.body,
  includeFontPadding: false,
};

export const globalFontStyle = {
  fontFamily: AppFont.regular,
  includeFontPadding: false,
};
