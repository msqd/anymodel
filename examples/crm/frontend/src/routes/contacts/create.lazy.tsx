import { createLazyFileRoute } from "@tanstack/react-router";
import toast from "react-hot-toast";
import { ContactForm } from "src/forms/contacts";

export const Route = createLazyFileRoute("/contacts/create")({
  component: RouteComponent,
});

function RouteComponent() {
  const navigate = Route.useNavigate();
  return (
    <main>
      <h1>Create Contact</h1>
      <ContactForm
        onSubmitSuccess={(data) => {
          toast("Contact created.", { icon: "🎉" });
          navigate({ to: `/contacts/${data.id}` });
        }}
      />
    </main>
  );
}
