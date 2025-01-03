
export const config = {
  header: true,
  headerNames: false,
  dateOneLiner: false,
  camiName: 'Osman Bey',
  prayerJson: '/osman_bey_prayer_times.json',
  dateJson: '/hijri_dates.json',
  quotes: true,
  ditib: true,
  showSabahNamazi: false,
  showAnnouncements: true,

  camiNameIdentifier: 'test-mosque',
  apiUrl: import.meta.env.VITE_API_URL,
  wsUrl: import.meta.env.VITE_WS_URL,
}