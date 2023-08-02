import { PluginComponentType, useActivePlugins } from "@fiftyone/plugins";
import { get } from "lodash";
import React, { useEffect } from "react";
import { getComponent, getErrorsForView } from "../utils";

export default function DynamicIO(props) {
  const { schema, onChange, path, parentSchema, relativePath } = props;
  const customComponents = useCustomComponents();
  const Component = getComponent(schema, customComponents);
  const computedSchema = schemaWithInheritedDefault(
    schema,
    parentSchema,
    relativePath
  );
  const { default: defaultValue, type } = computedSchema;

  // todo: need to improve initializing default value in state
  useEffect(() => {
    if (defaultValue) onChange(path, defaultValue);
    else if (type === "boolean") onChange(path, false);
  }, [defaultValue]);

  return (
    <Component
      {...props}
      schema={computedSchema}
      validationErrors={getErrorsForView(props)}
    />
  );
}

function useCustomComponents() {
  const pluginComponents =
    useActivePlugins(PluginComponentType.Component, {}) || [];

  return pluginComponents.reduce((componentsByName, component) => {
    componentsByName[component.name] = component.component;
    return componentsByName;
  }, {});
}

function schemaWithInheritedDefault(schema, parentSchema, path) {
  const providedDefault = get(schema, "default");
  const inheritedDefault = get(parentSchema, `default.${path}`);
  const computedDefault = providedDefault ?? inheritedDefault;
  return { ...schema, default: computedDefault };
}
