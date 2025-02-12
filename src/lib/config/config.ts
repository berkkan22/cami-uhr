
export const config = {
  header: false,
  headerNames: false,
  dateOneLiner: true,
  camiName: 'DITIB Lüneburg Merkez',
  prayerJson: '/time_data.json',
  dateJson: '/date_data.json',
  quotes: true,
  ditib: false,
  showSabahNamazi: true,
  showAnnouncements: true,
  changeIslamicDayOnMidnight: true,

  camiNameIdentifier: 'lueneburg-merkez-mosque',
  apiUrl: import.meta.env.VITE_API_URL,
  wsUrl: import.meta.env.VITE_WS_URL,
}