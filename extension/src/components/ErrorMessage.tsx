interface Props {
  message: string | null;
}

export default function ErrorMessage({ message }: Props) {
  if (!message) return null;
  return (
    <div className="alert" role="alert">
      {message}
    </div>
  );
}