import React, { useRef } from "react";
import { createRoot } from "react-dom/client";
import { RecoilRoot, useRecoilState } from "recoil";
import { RecoilRelayEnvironmentProvider } from "recoil-relay";
import { Dataset, getEnvProps, fos } from "./";
import { getFetchFunction } from "@fiftyone/utilities";

// import "./index.css";

//
// NOTE: this represents a "mock" environment that the Dataset
// component is embedded in. It is also used as a reference
// for the contract the embedding application must adhere to
//
const DatasetWrapper = () => {
  // @ts-ignore
  const props = getEnvProps();

  // @ts-ignore
  return (
    <RecoilRoot>
      <RecoilRelayEnvironmentProvider {...props}>
        <LoadableDataset />
      </RecoilRelayEnvironmentProvider>
    </RecoilRoot>
  );
};

const EXAMPLE_VIEW = [
  {
    _cls: "fiftyone.core.stages.Limit",
    kwargs: [["limit", 10]],
    _uuid: "020b33dd-775a-4b4a-a865-4901e2e6ee43",
  },
];

function LoadableDataset() {
  const [settings, setSettings] = React.useState({
    dataset: "quickstart",
    readOnly: false,
  });
  const [view, setView] = useRecoilState(fos.view);
  function printView() {
    console.log(JSON.stringify(view, null, 2));
  }

  function changeView() {
    setView(EXAMPLE_VIEW);
  }

  function clearView() {
    setView([]);
  }

  function saveView() {
    getFetchFunction()("POST", "/view", {
      dataset: "quickstart",
      view,
      name: "demo",
      description: "save with button",
    });
  }

  return (
    <>
      <DatasetSettings current={settings} onChange={setSettings} />
      <button onClick={() => printView()}>Print View</button>
      <button onClick={() => changeView()}>Set View</button>
      <button onClick={() => clearView()}>Clear View</button>
      <button onClick={() => saveView()}>Save View</button>
      <div style={{ height: "100vh", overflow: "hidden" }}>
        <Dataset datasetName={settings.dataset} readOnly={settings.readOnly} />
      </div>
    </>
  );
}

function DatasetSettings({ current, onChange }) {
  const datasetInputRef = useRef();
  const readOnlyInputRef = useRef();
  function load(e) {
    e.preventDefault();
    const dataset = datasetInputRef.current
      ? datasetInputRef.current.value
      : null;
    const readOnly = readOnlyInputRef.current
      ? readOnlyInputRef.current.checked
      : false;
    onChange((s) => ({ ...s, dataset, readOnly }));
  }
  return (
    <form onSubmit={load}>
      <input
        ref={readOnlyInputRef}
        type="checkbox"
        defaultChecked={current.readOnly}
      />{" "}
      Read Only
      <input ref={datasetInputRef} type="text" defaultValue={current.dataset} />
      <button type="submit">load</button>
    </form>
  );
}

createRoot(document.getElementById("root") as HTMLDivElement).render(
  <DatasetWrapper />
);
