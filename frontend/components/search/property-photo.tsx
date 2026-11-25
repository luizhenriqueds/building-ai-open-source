import Image from "next/image";
import { Badge } from "@/components/ui/badge";

type Props = { imageUrl: string | null; alt: string; discount: number | null };

export function PropertyPhoto({ imageUrl, alt, discount }: Props) {
  return (
    <div className="relative grid min-h-34 place-items-center bg-surface-3 text-sm text-muted-foreground">
      {imageUrl ? (
        <Image
          src={imageUrl}
          alt={alt}
          fill
          unoptimized
          sizes="11rem"
          className="object-cover"
        />
      ) : (
        <span>No photo</span>
      )}
      {discount !== null && discount > 0 && (
        <Badge className="absolute top-2 left-2 rounded-md bg-primary px-2.5 font-semibold text-primary-foreground">
          -{Math.round(discount)}%
        </Badge>
      )}
    </div>
  );
}
