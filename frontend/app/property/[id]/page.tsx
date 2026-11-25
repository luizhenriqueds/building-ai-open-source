import { PropertyView } from "@/components/property/property-view";

export default async function PropertyPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return <PropertyView id={id} />;
}
