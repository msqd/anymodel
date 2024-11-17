import { FieldApi, useForm } from "@tanstack/react-form";
import { InferType, object, string } from "yup";
import { yupValidator } from "@tanstack/yup-form-adapter";
import { useContactUpdateOrCreateMutation } from "src/queries/contacts";

const schema = object({
  first_name: string().min(3).required(),
  last_name: string().min(3).required(),
  email: string().email().required(),
});

type Contact = InferType<typeof schema>;

function FieldInfo({ field }: { field: FieldApi<any, any, any, any> }) {
  return (
    <>
      {field.state.meta.isTouched && field.state.meta.errors.length ? (
        <em>{field.state.meta.errors.join(",")}</em>
      ) : null}
      {field.state.meta.isValidating ? "Validating..." : null}
    </>
  );
}

export function ContactForm({
  onSubmitSuccess,
  initial,
}: {
  onSubmitSuccess: (data: any) => void;
  initial?: Contact & { id: number };
}) {
  const mutation = useContactUpdateOrCreateMutation();
  const form = useForm({
    defaultValues: {
      first_name: initial?.first_name || "",
      last_name: initial?.last_name || "",
      email: initial?.email || "",
    },
    onSubmit: async ({ value }) => {
      mutation.mutate(initial?.id ? { ...value, id: initial.id } : value, {
        onSuccess: onSubmitSuccess,
      });
    },
    validatorAdapter: yupValidator(),
    validators: { onChange: schema },
  });

  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        e.stopPropagation();
        form.handleSubmit();
      }}
    >
      <div>
        <form.Field
          name="first_name"
          children={(field) => (
            <>
              <label htmlFor={field.name}>First Name:</label>{" "}
              <input
                id={field.name}
                name={field.name}
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              <FieldInfo field={field} />
            </>
          )}
        />
      </div>

      <div>
        <form.Field
          name="last_name"
          children={(field) => (
            <>
              <label htmlFor={field.name}>Last Name:</label>{" "}
              <input
                id={field.name}
                name={field.name}
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              <FieldInfo field={field} />
            </>
          )}
        />
      </div>

      <div>
        <form.Field
          name="email"
          children={(field) => (
            <>
              <label htmlFor={field.name}>Email:</label>{" "}
              <input
                id={field.name}
                name={field.name}
                type="email"
                value={field.state.value}
                onBlur={field.handleBlur}
                onChange={(e) => field.handleChange(e.target.value)}
              />
              <FieldInfo field={field} />
            </>
          )}
        />
      </div>

      <form.Subscribe
        selector={(state) => [state.canSubmit, state.isSubmitting]}
        children={([canSubmit, isSubmitting]) => (
          <>
            <button type="submit" disabled={!canSubmit}>
              {isSubmitting ? "..." : "Submit"}
            </button>
            <button type="reset" onClick={() => form.reset()}>
              Reset
            </button>
          </>
        )}
      />
    </form>
  );
}
