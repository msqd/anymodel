import { createLazyFileRoute } from "@tanstack/react-router";
import { useContactGetQuery } from "src/queries/contacts";
import { useState } from "react";
import { ContactForm } from "../../forms/contacts.tsx";
import toast from "react-hot-toast";
import { useQueryClient } from "@tanstack/react-query";

export const Route = createLazyFileRoute("/contacts/$id")({
  component: RouteComponent,
});

function RouteComponent() {
  const { id } = Route.useParams();
  const query = useContactGetQuery(id);
  const queryClient = useQueryClient();
  const [isEditing, setIsEditing] = useState(false);

  if (query.isLoading) {
    return "Loading...";
  }
  if (query.isError) {
    return `An error has occurred.`;
  }

  const contact = query.data;

  return (
    <main>
      <h1>
        {contact.first_name} {contact.last_name}
      </h1>
      {isEditing ? (
        <div>
          <ContactForm
            onSubmitSuccess={(data) => {
              toast(`Contact updated (#${data.id}).`, { icon: "🎉" });
              queryClient.setQueryData(["contact", `${data.id}`], data);
              setIsEditing(false);
            }}
            initial={contact}
          />
        </div>
      ) : (
        <>
          <ul>
            <li>First Name: {contact.first_name}</li>
            <li>Last Name: {contact.last_name}</li>
            <li>Email: {contact.email}</li>
          </ul>
          <button onClick={() => setIsEditing(true)}>edit</button>
        </>
      )}
    </main>
  );
}
