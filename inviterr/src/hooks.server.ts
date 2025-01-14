import { env } from '$env/dynamic/private';
import { MongoClient } from 'mongodb';


const mongoClient = new MongoClient(env.MONGO_URL ?? 'mongodb://localhost:27017');


export async function handle({ event, resolve }: { event: any; resolve: Function; }) {
  await mongoClient.connect();

  const mongoDb = mongoClient.db(env.MONGO_DB ?? 'inviterr');

  event.locals.mongo = mongoDb;
  return await resolve(event);
}