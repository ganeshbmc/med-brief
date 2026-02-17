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

/**
 * Format ISO datetime or YYYY-MM-DD as DD-MM-YYYY
 * @param {string} dateTimeStr - DateTime string
 * @returns {string} Formatted date string
 */
export function formatDateTimeDisplay(dateTimeStr) {
  if (!dateTimeStr) return '';
  const datePart = dateTimeStr.includes('T') ? dateTimeStr.split('T')[0] : dateTimeStr;
  return formatDateDisplay(datePart);
}

/**
 * Calculate days ago from now based on a date or datetime
 * @param {string} dateTimeStr - DateTime string
 * @returns {number} Days ago
 */
export function daysAgoFromNow(dateTimeStr) {
  if (!dateTimeStr) return 0;
  const datePart = dateTimeStr.includes('T') ? dateTimeStr.split('T')[0] : dateTimeStr;
  const [year, month, day] = datePart.split('-').map(Number);
  if (!year || !month || !day) return 0;

  const targetDate = new Date(Date.UTC(year, month - 1, day));
  const now = new Date();
  const todayUtc = new Date(Date.UTC(now.getUTCFullYear(), now.getUTCMonth(), now.getUTCDate()));
  const diffMs = todayUtc.getTime() - targetDate.getTime();
  const diffDays = Math.floor(diffMs / (1000 * 60 * 60 * 24));
  return diffDays < 0 ? 0 : diffDays;
}
