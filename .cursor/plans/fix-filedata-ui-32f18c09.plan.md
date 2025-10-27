<!-- 32f18c09-ebf7-4100-aea4-8866d4d6b25c 05a008d1-7128-423d-ac05-9515618ef10e -->
# Fix FileData Structure in Deep Agents UI

## Problem

The UI is treating files as `Record<string, string>` when the backend actually sends `Record<string, FileData>` where FileData contains `{content: string[], created_at: string, modified_at: string}`. This causes a runtime error when clicking on files in the UI.

## Solution

### 1. Update Type Definitions

**File**: `/Users/suresh/scm/github.com/langchain-ai/deep-agents-ui/src/app/types/types.ts`

- Add `FileData` interface matching the backend structure:
  ```typescript
  export interface FileData {
    content: string[];
    created_at: string;
    modified_at: string;
  }
  ```

- Keep `FileItem` as-is (it's the UI-facing interface)
- Add a helper type for the actual state structure

### 2. Update State Handling in useChat Hook

**File**: `/Users/suresh/scm/github.com/langchain-ai/deep-agents-ui/src/app/hooks/useChat.ts`

- Change `StateType` to use `Record<string, FileData>` instead of `Record<string, string>` (line 13)
- Update the callback to convert FileData to plain strings when notifying parent components (lines 41-43)

### 3. Update Page Component

**File**: `/Users/suresh/scm/github.com/langchain-ai/deep-agents-ui/src/app/page.tsx`

- Update state fetching logic to handle FileData objects (lines 45-50)
- Convert FileData objects to strings when setting the files state
- Add helper function to convert FileData to string (join the content array)

### 4. Update TasksFilesSidebar Component

**File**: `/Users/suresh/scm/github.com/langchain-ai/deep-agents-ui/src/app/components/TasksFilesSidebar/TasksFilesSidebar.tsx`

- The component already expects `Record<string, string>` which is correct for the UI layer
- No changes needed here since the conversion happens at the page level

### 5. Verification

- Ensure FileViewDialog works with plain string content (already does)
- Test file click functionality
- Verify backward compatibility if needed

### To-dos

- [ ] Add FileData interface to types.ts matching backend structure
- [ ] Update useChat hook to handle FileData objects and convert to strings
- [ ] Update page.tsx to convert FileData objects when fetching thread state
- [ ] Verify file view dialog works correctly with the changes