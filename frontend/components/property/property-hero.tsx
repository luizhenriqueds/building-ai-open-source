import Image from "next/image";

type Props = { imageUrl: string | null; alt: string };

export function PropertyHero({ imageUrl, alt }: Props) {
  return (
    <div className="relative grid aspect-video place-items-center overflow-hidden rounded-xl border border-input bg-surface-3 text-muted-foreground">
      {imageUrl ? (
        <Image
          src={imageUrl}
          alt={alt}
          fill
          unoptimized
          priority
          sizes="(min-width: 1024px) 44rem, 100vw"
          className="object-cover"
        />
      ) : (
        <span>No photo</span>
      )}
    </div>
  );
}
