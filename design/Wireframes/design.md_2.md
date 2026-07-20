---
name: Hardware Tracker
colors:
  surface: '#fff8f6'
  surface-dim: '#efd5ca'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff1eb'
  surface-container: '#ffeae1'
  surface-container-high: '#fee3d8'
  surface-container-highest: '#f8ddd2'
  on-surface: '#261812'
  on-surface-variant: '#5a4136'
  inverse-surface: '#3d2d26'
  inverse-on-surface: '#ffede6'
  outline: '#8e7164'
  outline-variant: '#e2bfb0'
  surface-tint: '#a04100'
  primary: '#a04100'
  on-primary: '#ffffff'
  primary-container: '#ff6b00'
  on-primary-container: '#572000'
  inverse-primary: '#ffb693'
  secondary: '#5f5e5e'
  on-secondary: '#ffffff'
  secondary-container: '#e2dfde'
  on-secondary-container: '#636262'
  tertiary: '#5d5e60'
  on-tertiary: '#ffffff'
  tertiary-container: '#98999b'
  on-tertiary-container: '#2f3133'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdbcc'
  primary-fixed-dim: '#ffb693'
  on-primary-fixed: '#351000'
  on-primary-fixed-variant: '#7a3000'
  secondary-fixed: '#e5e2e1'
  secondary-fixed-dim: '#c8c6c5'
  on-secondary-fixed: '#1c1b1b'
  on-secondary-fixed-variant: '#474746'
  tertiary-fixed: '#e2e2e4'
  tertiary-fixed-dim: '#c6c6c8'
  on-tertiary-fixed: '#1a1c1d'
  on-tertiary-fixed-variant: '#454749'
  background: '#fff8f6'
  on-background: '#261812'
  surface-variant: '#f8ddd2'
  success: '#22C55E'
  danger: '#E63946'
  text-muted: '#6B7280'
  border: '#E5E7EB'
  hero-gradient-start: '#FFFFFF'
  hero-gradient-end: '#FFF4EC'
typography:
  headline-hero:
    fontFamily: Inter
    fontSize: 64px
    fontWeight: '700'
    lineHeight: '1.1'
    letterSpacing: -0.02em
  headline-section:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-card:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-main:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-nav:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.2'
  label-small:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: '1.2'
  badge:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '500'
    lineHeight: '1'
    letterSpacing: 0.02em
  headline-hero-mobile:
    fontFamily: Inter
    fontSize: 40px
    fontWeight: '700'
    lineHeight: '1.1'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  container-max: 1440px
  margin-desktop: 80px
  gutter: 24px
  section-padding: 80px
  card-padding: 20px
---

## Brand & Style

The design system is built for a high-performance hardware ecosystem, targeting enthusiasts, gamers, and PC builders. The aesthetic is **High-Tech Corporate Modern**: a fusion of clean, functional layouts with high-energy accents. It prioritizes clarity and data density while maintaining a premium, trustworthy feel.

The brand personality is authoritative yet accessible, using whitespace to organize complex technical specifications. Visual interest is generated through precise geometry, subtle gradients, and a signature high-contrast accent color that guides the user through the building and tracking journey.

## Colors

The palette is anchored by a vibrant **Primary Orange**, used strategically for high-conversion actions and key brand touchpoints. The background strategy utilizes a tiered grayscale to separate content blocks, moving from pure white for cards to a soft off-gray for secondary sections.

- **Primary:** Reserved for CTAs, statistics, and interactive states.
- **Secondary/Neutral:** Deep charcoal and graphite tones for typography and structural elements like footers.
- **Semantic:** Success green is used for compatibility and discounts, while danger red handles errors and hardware incompatibilities.
- **Surfaces:** Use the hero gradient (White to soft peach) sparingly behind lead messaging to soften the technical edge.

## Typography

The design system utilizes **Inter** exclusively to lean into its systematic, utilitarian nature. The type scale is optimized for readability within complex data tables and hardware lists.

- **Headlines:** Large, bold weights are used for hero sections with slight negative letter-spacing to enhance the high-tech impact.
- **Body:** Standardized at 16px for optimal legibility during long research sessions.
- **Labels & Badges:** Slightly tighter and bolder to distinguish metadata from descriptive text.
- **Scale:** On mobile devices, the Hero H1 should downscale significantly (40px) to ensure titles do not break awkwardly across lines.

## Layout & Spacing

The layout follows a **Fixed Grid** philosophy for desktop, capping content width at 1440px to maintain line length readability and professional structure. 

- **Grid:** A 12-column grid is the standard for all page templates.
- **Spacing Rhythm:** Vertical section spacing is generous (80px) to allow the "clean/modern" aesthetic to breathe.
- **Internal Spacing:** Components like cards use a 20px internal padding with 24px gaps between siblings, creating a tight but clear information hierarchy.
- **Responsiveness:** For tablet and mobile, the side margins contract to 24px and 16px respectively, with the 12-column grid collapsing into 4 columns for mobile views.

## Elevation & Depth

This design system uses **Tonal Layers** combined with **Ambient Shadows** to create a sense of organized depth.

- **Base Elevation:** Most cards sit on the background with a subtle, diffused shadow (`0 2px 12px rgba(0,0,0,0.08)`) and a light 1px border. This ensures clear boundaries even on white backgrounds.
- **Interactive Depth:** On hover, elements utilize a "Glow Shadow" technique where the primary color is lightly tinted into the shadow (`0 8px 24px rgba(255, 107, 0, 0.12)`). This provides a technical "light-up" effect.
- **Sectioning:** Alternating `bg-base` and `bg-section` surfaces provides macro-level depth without requiring additional shadows or borders.

## Shapes

The shape language is consistently **Rounded**, striking a balance between approachable modern design and the rigid geometry of hardware components.

- **Standard (8px):** Applied to buttons, input fields, and small UI controls.
- **Large (12px):** Applied to Product and Build cards to soften the data-heavy content.
- **Pill (14px+):** Applied to Badges and Tags to make them distinct from other rectangular UI elements.
- **Inputs:** Maintain a consistent 8px radius to match buttons, creating a unified form-factor for all interactive elements.

## Components

### Buttons
- **Primary:** Solid #FF6B00 background with white text. No border. Height: 48px (L), 36px (M).
- **Secondary:** Dark neutral background (#1A1A1A) with light text and subtle border. 
- **Ghost:** Transparent background with Primary #FF6B00 border and text.

### Cards
- **Product Card:** Elevated white surface with a 1px border. Features a clear hierarchy: Image (top), Metadata (middle), Price/CTA (bottom). Use success badges for discounts.
- **Build Card:** Larger format, emphasizing the "Preview" image. Includes a footer with "Likes" and "Author" metadata in `text-muted`.

### Badges / Tags
- Use a tinted background approach (20% opacity of the semantic color) with a 40% opacity border of the same hue. This keeps badges legible but less visually heavy than solid blocks.

### Inputs
- Specialized for high-tech aesthetics: Deep neutral backgrounds (#0D0D0F) or white with subtle borders. The focus state must use a Primary #FF6B00 1px border to signal activity clearly.

### Stats Strip
- High-impact component with a solid Primary #FF6B00 background and white typography. Used to highlight global tracker stats (e.g., "Active Builds", "Price Drops Today").