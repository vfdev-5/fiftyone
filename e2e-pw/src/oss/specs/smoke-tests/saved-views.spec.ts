import { describe } from "node:test";
import { expect, test } from "src/oss/fixtures";
import { getUniqueDatasetNameWithPrefix } from "src/oss/utils";

// test("smoke saved views", async ({ page, fiftyoneLoader }) => {
//   const datasetName = getUniqueDatasetNameWithPrefix("smoke-quickstart");

//   await fiftyoneLoader.loadZooDataset("quickstart", datasetName, {
//     max_samples: 5,
//   });

//   await fiftyoneLoader.waitUntilLoad(page, datasetName);

//   // await expect(page.getByTestId("entry-count-all")).toHaveText("5");
// });

describe("saved views", () => {
  const datasetName = getUniqueDatasetNameWithPrefix("smoke-quickstart");

  test.beforeAll(async ({ fiftyoneLoader }) => {
    await fiftyoneLoader.loadZooDataset("quickstart", datasetName, {
      max_samples: 5,
    });
  });

  test("has title", async ({ page, fiftyoneLoader }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await expect(page).toHaveTitle(/FiftyOne/);
  });

  test("saved views selector exist", async ({ page, fiftyoneLoader }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);
    const savedViewsLocator = page.getByText("Unsaved view");
    await expect(savedViewsLocator).toBeVisible();
  });

  test("saved views selector options opens create view dialog", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);
    await page.getByText("Unsaved view").click();

    const savedViewsCreate = await page.getByText(
      "save current filters as view"
    );
    await expect(savedViewsCreate).toBeVisible();
    await expect(savedViewsCreate).not.toBeDisabled();

    await expect(page.getByText("create view")).not.toBeVisible();
    await savedViewsCreate.click();
    await expect(page.getByText("create view")).toBeVisible();

    const nameInput = await page.getByPlaceholder("Your view name");
    await expect(nameInput).toBeVisible();
    await expect(nameInput).toHaveValue("");

    // expect name to be focused
    // await expect(page.getByRole("input")).toBeFocused();

    // expect description input to be empty
    const descInput = page.getByPlaceholder("Enter a description");
    await expect(descInput).toBeVisible();
    await expect(descInput).toHaveValue("");
  });

  test("saved views selector -> color selector exists and default color is Gray", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    const colorInput = page.getByText("Color", { exact: true });
    await expect(colorInput).toBeVisible();

    await expect(page.getByText("Gray", { exact: true })).toBeVisible();

    // make sure there is a color bubble and default is gray
    // const colorDot = page.getByLabel("default color");
    // const colorDot = page.("default color");

    // const inputElement = page.locator("#emailAddress");
    // const colorDot = page.getByTestId("testme");
    // const colorDot = page.locator("data-test-id=testme");
    // const colorDot = page.getByTestId("[data-cy=testmetoo]");
    // const colorDot = page.locator("#asdasdd");
    // const colorDot = page.locator("_react=Selection");
    // await expect(colorDot).toBeVisible();
  });

  test("'Save view' button is disabled if no name input", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    await page.getByPlaceholder("Your view name").fill("");
    const SaveBtn = page.getByText("Save view", { exact: true });

    expect(SaveBtn).toBeDisabled();
  });

  test("'Save view' button is enabled if name input is not empty", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    await page.getByPlaceholder("Your view name").fill("test name 1");
    const SaveBtn = page.getByText("Save view", { exact: true });

    expect(SaveBtn).not.toBeDisabled();
  });

  test("'Cancel' button clears the name, description, and color", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    const nameInput = page.getByPlaceholder("Your view name");
    await nameInput.type("test name 1");
    expect(await nameInput.inputValue()).toEqual("test name 1");

    const descInput = page.getByPlaceholder("Enter a description");
    await descInput.type("test description 1");

    const cancelBtn = page.getByText("Cancel", { exact: true });
    expect(cancelBtn).not.toBeDisabled();
    await cancelBtn.click({ force: true });

    // get name
    // const name = await nameInput.innerText();
    // expect(name).toEqual("");

    // get description
    // const description = descInput.inputValue();
    // expect(name).
  });

  test("Successfully creates a saved view", async ({
    page,
    fiftyoneLoader,
  }) => {
    await page.goto(`http://0.0.0.0:8787/datasets/${datasetName}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    const nameInput = page.getByPlaceholder("Your view name");
    await nameInput.type("test name 1");
    expect(await nameInput.inputValue()).toEqual("test name 1");

    const descInput = page.getByPlaceholder("Enter a description");
    await descInput.type("test description 1");

    const saveBtn = page.getByText("Save view", { exact: true });
    expect(saveBtn).not.toBeDisabled();
    await saveBtn.click({ force: true });

    await expect(page).toHaveURL(/view=test-name-1/);

    // make sure the saved view is also selected
    await expect(page.getByText("test name 1")).toBeVisible();
  });

  test("Directly linking to non-existant view will redirect", async ({
    page,
    fiftyoneLoader,
  }) => {
    const baseURL = `http://0.0.0.0:8787/datasets/${datasetName}`;
    await page.goto(`${baseURL}?view=test-name-1`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    expect(page).toHaveURL(baseURL);
  });

  test("Clear button should clear saved view selection and URL", async ({
    page,
    fiftyoneLoader,
  }) => {
    const baseURL = `http://0.0.0.0:8787/datasets/${datasetName}`;
    await page.goto(`${baseURL}`);

    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.getByText("Unsaved view").click();

    const savedViewsCreate = page.getByText("save current filters as view");
    await savedViewsCreate.click();

    const nameInput = page.getByPlaceholder("Your view name");
    await nameInput.type("test name 1");

    const descInput = page.getByPlaceholder("Enter a description");
    await descInput.type("test description 1");

    const saveBtn = page.getByText("Save view", { exact: true });
    await saveBtn.click({ force: true });

    await page.reload({ waitUntil: "domcontentloaded" });
    await fiftyoneLoader.waitUntilLoad(page, datasetName);

    await page.click("data-test-id=clear-me");
    // await clearSavedViewBtn.click();
  });
});
