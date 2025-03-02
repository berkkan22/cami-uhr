
export const config = {
  header: true,
  headerNames: false,
  dateOneLiner: false,
  camiName: 'Osman Bey',
  prayerJson: '/time_data.json',
  dateJson: '/date_data.json',
  quotes: true,
  ditib: true,
  showSabahNamazi: false,
  showAnnouncements: true,
  changeIslamicDayOnMidnight: false,

  camiNameIdentifier: 'osman-bey-mosque',
  apiUrl: import.meta.env.VITE_API_URL,
  wsUrl: import.meta.env.VITE_WS_URL,
}