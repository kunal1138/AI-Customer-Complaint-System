import { createSlice, createAsyncThunk } from '@reduxjs/toolkit';
import { submitTextComplaint, submitFileComplaint, fetchComplaints } from '../api/complaintsApi';

export const processTextComplaint = createAsyncThunk(
  'complaints/processText',
  async (text) => await submitTextComplaint(text)
);

export const processFileComplaint = createAsyncThunk(
  'complaints/processFile',
  async (file) => await submitFileComplaint(file)
);

export const loadComplaintHistory = createAsyncThunk(
  'complaints/loadHistory',
  async () => await fetchComplaints()
);

const initialState = {
  status: 'idle', // idle | loading | succeeded | failed
  error: null,
  currentResult: null, // the most recently processed complaint (drives the form + AI panel)
  history: [],
  historyStatus: 'idle',
};

const complaintsSlice = createSlice({
  name: 'complaints',
  initialState,
  reducers: {
    clearCurrentResult(state) {
      state.currentResult = null;
      state.status = 'idle';
      state.error = null;
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(processTextComplaint.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(processTextComplaint.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.currentResult = action.payload;
      })
      .addCase(processTextComplaint.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(processFileComplaint.pending, (state) => {
        state.status = 'loading';
        state.error = null;
      })
      .addCase(processFileComplaint.fulfilled, (state, action) => {
        state.status = 'succeeded';
        state.currentResult = action.payload;
      })
      .addCase(processFileComplaint.rejected, (state, action) => {
        state.status = 'failed';
        state.error = action.error.message;
      })
      .addCase(loadComplaintHistory.pending, (state) => {
        state.historyStatus = 'loading';
      })
      .addCase(loadComplaintHistory.fulfilled, (state, action) => {
        state.historyStatus = 'succeeded';
        state.history = action.payload;
      })
      .addCase(loadComplaintHistory.rejected, (state) => {
        state.historyStatus = 'failed';
      });
  },
});

export const { clearCurrentResult } = complaintsSlice.actions;
export default complaintsSlice.reducer;
