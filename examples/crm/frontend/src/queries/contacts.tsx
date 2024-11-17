import { useMutation, useQuery } from "@tanstack/react-query";

export function useContactListQuery() {
  return useQuery({
    queryKey: ["contacts"],
    queryFn: async () => {
      const response = await fetch("http://localhost:3001/");
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
  });
}

export function useContactGetQuery(id: string) {
  return useQuery({
    queryKey: ["contact", id],
    queryFn: async () => {
      const response = await fetch(`http://localhost:3001/${id}`);
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
  });
}

export function useContactUpdateOrCreateMutation() {
  return useMutation({
    mutationFn: async (contact: any) => {
      const response = await fetch(
        contact.id
          ? `http://localhost:3001/${contact.id}`
          : "http://localhost:3001/",
        {
          method: contact.id ? "PUT" : "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(contact),
        },
      );

      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      return response.json();
    },
  });
}
