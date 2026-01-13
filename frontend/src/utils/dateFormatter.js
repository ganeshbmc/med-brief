/**
 * Convert YYYY-MM-DD to DD-MM-YYYY format
 * @param {string} dateStr - Date string in YYYY-MM-DD format
 * @returns {string} Date string in DD-MM-YYYY format
 */
export function formatDateDisplay(dateStr) {
  if (!dateStr) return '';
  
  // Handle YYYY-MM-DD format
  if (dateStr.includes('-')) {
    const parts = dateStr.split('-');
    if (parts.length === 3) {
      const [year, month, day] = parts;
      return `${day}-${month}-${year}`;
    }
  }
  
  // Handle other date formats from PubMed (return as-is for now)
  return dateStr;
}

/**
 * Format date range for display
 * @param {string} fromDate - Start date in YYYY-MM-DD
 * @param {string} toDate - End date in YYYY-MM-DD  
 * @returns {string} Formatted date range
 */
export function formatDateRange(fromDate, toDate) {
  return `${formatDateDisplay(fromDate)} to ${formatDateDisplay(toDate)}`;
}
