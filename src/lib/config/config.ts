
export const config = {
  header: true,
  headerNames: true,
  dateOneLiner: true,
  camiName: 'Hz. Ömer',
  prayerJson: '/time_data.json',
  dateJson: '/date_data.json',
  quotes: true,
  ditib: true,
  showSabahNamazi: false,
  showAnnouncements: false,
  changeIslamicDayOnMidnight: false,

  camiNameIdentifier: 'schwarzenbek-mosque',
  apiUrl: import.meta.env.VITE_API_URL,
  wsUrl: import.meta.env.VITE_WS_URL,
}